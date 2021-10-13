import datetime

import xlsxwriter
from django.http import HttpResponse
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.error_response import FORBIDDEN_RESPONSE
from core.utils import access_permissions
from ultratech_new_destination import modelscript
from ultratech_new_destination.constants import PLANTMAPDATA_MAPPER, SIMILARITYDATA_MAPPER, \
    REFDATA_MAPPER, NEARESTPOINTS_MAPPER
from ultratech_new_destination.models import Destination, RefData, PlantMapData, NearestPoints, SimilarityData, \
    MapAPIData

from ultratech_new_destination.modelscript import function1, \
    Plant_Lat_Long, get_data_from_db, Geocode_latlong, key, gmap_api_count, map_data
from ultratech_new_destination.serializers import DestinationSerializers, RefDataSerializer, PlantMapDataSerializers, \
    SimilarityDataSerializers, NearestPointsSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

import logging

from ultratech_new_destination.utils import get_data, format_filter_response, check_plant_access, \
    get_allowed_plants, populate_xlxs

import numpy as np

LOGGER = logging.getLogger('django')


class DestinationView(ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializers

    @access_permissions(('ultratech',))
    def create(self, request, *args, **kwargs):
        """
        create new destination by running modelscript
        :param request: request will have
            plant: contains plant name and plant code,
            destination: address of destiantion
            taluka: contains taluka code and taluka name
            truck_type
            direct_sto
            similarity: either 1 or 0
        :param args:
        :param kwargs:
        :return: after running model script get frames, save those frames in DB and that data
        """
        try:
            LOGGER.info("Executing new destination")
            plant = request.data.get('plant')
            plant_name = plant[5:]
            plant = plant[0:4]
            if not check_plant_access(request.user, plant):  # checking user have requested plant access
                return Response(status=HTTP_403_FORBIDDEN, data={**FORBIDDEN_RESPONSE.get("PLANT_ACCESS_DENIED"), "message":"No plant access"})
            destination = request.data.get('destination')
            taluka = request.data.get('taluka')
            taluka_name = taluka.split('-')[1]
            truck_type = request.data.get('truck_type')
            direct_sto = request.data.get('direct_sto')
            similarity = int(request.data.get('similarity'))
            try:

                waypoints = request.data.get('waypoints')
                if type(waypoints) == str:
                    waypoints = eval(waypoints)
            except:
                waypoints = []
            waypoints = np.array(waypoints)
            lead = int(request.data.get('lead')) if request.data.get('lead') else None
            get_data_from_db(plant,taluka)  # Load data from DB, required to run model script
            from ultratech_new_destination.modelscript import bf
            plant_lat_long = Plant_Lat_Long(plant, bf=bf)
            LOGGER.info("get plant_lat_long")
            plant_lat = plant_lat_long.get('Source_Lat').values[0]
            plant_long = plant_lat_long.get('Source_Long').values[0]
            lat_long = Geocode_latlong(destination, key)
            destination_lat, destination_long = lat_long[0], lat_long[1]
            LOGGER.info("plant_lat={} plant_long={} destination_lat={} destination_long={}".format(plant_lat,
                                                                                                   plant_long,
                                                                                                   destination_lat,
                                                                                                   destination_long))
            plant_destination = self.queryset.filter(source_lat=plant_lat, source_long=plant_long,
                                                     new_destination_lat=destination_lat,
                                                     new_destination_long=destination_long,
                                                     taluka=taluka,
                                                     direct_sto=direct_sto,
                                                     similarity=similarity,
                                                     truck_type=truck_type
                                                     ) \
                .prefetch_related('map_data',
                                  'similarity_data',
                                  'ref_data',
                                  'nearest_points')
            LOGGER.info("plant_destination exists {}".format(plant_destination.exists()))
            response_data = {}
            if plant_destination.exists():
                map_api_data = MapAPIData.objects.filter(plant_destination=plant_destination.first())
                if map_api_data.exists():
                    map_api_data = map_api_data.first()
                    LOGGER.info("get map_api_data {}".format(map_api_data.id))
                    modelscript.map_data = {
                        'distance_matrix': map_api_data.distance_matrix,
                        'elev_url': map_api_data.elev_url,
                        'elevation_extraction': map_api_data.elevation_extraction,
                        'reverse_geocode': map_api_data.reverse_geocode
                    }

            LOGGER.info(
                "(plant {}, taluka_name {}, truck_type {}, direct_sto {}, destination {}, similarity {}, plant_name"
                " {}, taluka {})".format(plant, taluka_name, truck_type, direct_sto, destination, similarity,
                                         plant_name, taluka))
            try:
                model_result, map_data_result = function1(plant, taluka_name, truck_type, direct_sto, destination,
                                                          similarity,
                                                          plant_name, taluka,waypoints=waypoints,Lead=lead)
            except Exception as ex:
                LOGGER.exception("Exception in modelscript ")
                self.set_map_data_values()
                return Response(status=HTTP_400_BAD_REQUEST, data="unable to compute")
            LOGGER.info("model run completed")
            ref_data_frame = model_result[0]
            map_data_frame = model_result[2]
            nearest_data_frame = model_result[1]
            plant_destination = plant_destination.first()
            LOGGER.info("get data frame")
            if not plant_destination:
                plant_destination = Destination.objects.create(source_lat=map_data_frame.SOURCE_LAT,
                                                               source_long=map_data_frame.SOURCE_LONG,
                                                               new_destination_lat=map_data_frame.DESTINATION_LAT,
                                                               new_destination_long=map_data_frame.DESTINATION_LONG,
                                                               request_user=request.user.username,
                                                               truck_type=truck_type,
                                                               taluka=taluka,
                                                               direct_sto=direct_sto,
                                                               similarity=similarity)
            if not modelscript.map_data:
                MapAPIData.objects.create(plant_destination=plant_destination,
                                          distance_matrix=map_data_result['distance_matrix'],
                                          elev_url=map_data_result['elev_url'],
                                          elevation_extraction=map_data_result['elevation_extraction'],
                                          reverse_geocode=map_data_result['reverse_geocode'])

            self.delete_already_existing_frame(plant_destination)

            self.populate_db(ref_data_frame, plant_destination, RefData, response_data)
            self.populate_db(map_data_frame, plant_destination, PlantMapData, response_data)
            self.populate_db(nearest_data_frame, plant_destination, NearestPoints, response_data)

            if similarity == True:
                simi_data_frame = model_result[3]
                if str(simi_data_frame.PLANT.values[0]) != 'nan':
                    self.populate_db(simi_data_frame, plant_destination, SimilarityData, response_data)
                else:
                    LOGGER.info("simi_data_frame is nan")

            response_data['is_cached'] = True if modelscript.map_data else False
            self.set_map_data_values()
            response_data['plant_destination'] = plant_destination.id
            LOGGER.info("Total gmap api count = {}".format(modelscript.gmap_api_count))
            LOGGER.info("=====================")
            return Response(data=response_data)
        except Exception as ex:
            LOGGER.exception("Exception in DestinationView ")
            self.set_map_data_values()
            return Response(status=HTTP_400_BAD_REQUEST)

    def populate_db(self, data_frame, plant_destination, model_name, response):
        """
        parse data comes from modelscript in frames into table and save them
        :param data_frame: actual data
        :param plant_destination: foreign key for Destination table
        :param model_name: model object in which data need to be saved
        :param response:
        :return:
        """
        LOGGER.info("populating {}".format(model_name))
        data_dict = [{data_frame.columns[
                          i - 1].lower() if model_name.__name__ != PlantMapData.__name__ else PLANTMAPDATA_MAPPER.get(
            data_frame.columns[i - 1]): row[i] if str(row[i]) != 'nan' else None for i in range(1, len(row))} for row in
                     data_frame.itertuples()]
        data_obj = list()
        response[model_name.__name__] = data_dict
        for data in data_dict:
            data['plant_destination'] = plant_destination
            data_obj.append(model_name(**data))
            data.pop('plant_destination')
        model_name.objects.bulk_create(data_obj)
        LOGGER.info("populating done {}".format(model_name))

    def set_map_data_values(self):
        modelscript.map_data = None
        modelscript.map_data_result = {
            'distance_matrix': dict(),
            'elev_url': dict(),
            'elevation_extraction': dict(),
            'reverse_geocode': dict()
        }

    def delete_already_existing_frame(self, plant_destination):
        """
        delete already existing data of PlantMapData, SimilarityData, RefData, NearestPoints so that new data
        is saved without redundancy
        :param plant_destination: Destination object
        :return:
        """
        plant_destination.map_data.all().delete()
        plant_destination.similarity_data.all().delete()
        plant_destination.ref_data.all().delete()
        plant_destination.nearest_points.all().delete()
        LOGGER.info("already existing data deleted successfully")

    @access_permissions(('ultratech',))
    @action(detail=False, url_path='filter', methods=['get'])
    def new_destination_filter(self, request, *args, **kwargs):
        """
        send data to show in filers
        :param request: have delvry_plant, taluka, truck_type
        :param args:
        :param kwargs:
        :return:
        """
        delvry_plant = request.GET.get('delvry_plant')
        taluka = request.GET.get('taluka')
        truck_type = request.GET.get('truck_type')
        select_fields = ['b.plant_code', 'b.plant_desc']
        where_fields = dict()
        where_in_fields = dict()
        if delvry_plant:
            where_fields['b.plant_code'] = delvry_plant.split('-')[0]
            if not check_plant_access(request.user, where_fields['b.plant_code']):
                return Response(status=HTTP_403_FORBIDDEN, data=FORBIDDEN_RESPONSE.get("PLANT_ACCESS_DENIED"))
        else:
            where_in_fields['b.plant_code'] = tuple(str(plant) for plant in get_allowed_plants(request.user))

        plant_columnnames, plant_result_data = get_data(select_fields, where_fields, where_in_fields)

        select_fields = ['a.truck_type']
        where_fields = dict()
        where_in_fields = dict()
        if truck_type:
            where_fields['truck_type'] = truck_type

        truck_type_columnnames, truck_type_result_data = get_data(select_fields, where_fields, where_in_fields)

        select_fields = ['a.i2_taluka', 'a.i2_taluka_desc']
        where_fields = dict()
        where_in_fields = dict()
        if taluka:
            where_fields['i2_taluka'] = taluka.split('-')[0]

        taluka_type_columnnames, taluka_type_result_data = get_data(select_fields, where_fields, where_in_fields)

        # columnnames, result_data = get_data(select_fields, where_fields, where_in_fields)
        response = format_filter_response(plant_columnnames, plant_result_data, ['delvry_plant'], {})
        response = format_filter_response(truck_type_columnnames, truck_type_result_data, ['truck_type'], response)
        response = format_filter_response(taluka_type_columnnames, taluka_type_result_data, ['taluks'], response)
        if not response.get('delvry_plant'):
            return Response(status=HTTP_403_FORBIDDEN, data=FORBIDDEN_RESPONSE.get('NO_PLANT_ACCESS'))

        return Response(response)

    @access_permissions(('ultratech',))
    @action(detail=False, url_path='download', methods=['get'])
    def download(self, request, *args, **kwargs):
        """
        api to download destination data in xsls format which have data from PlantMapData, SimilarityData,
         RefData, NearestPoints
        :param request: have id of Destination for which you want to download data
        :param args:
        :param kwargs:
        :return:
        """
        destination_plant_id = request.GET.get('id')
        plant_destination = self.queryset.filter(pk=destination_plant_id) \
            .prefetch_related('map_data',
                              'similarity_data',
                              'ref_data',
                              'nearest_points')
        if not plant_destination.exists():
            return Response(status=HTTP_400_BAD_REQUEST, data="wrong id")
        plant_destination = plant_destination.first()
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename={filename}.xlsx'. \
            format(filename="new destination")
        row, col = 0, 0
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})

        populate_xlxs(workbook, PLANTMAPDATA_MAPPER, 'map_data', plant_destination)
        populate_xlxs(workbook, SIMILARITYDATA_MAPPER, 'similarity_data', plant_destination)
        populate_xlxs(workbook, REFDATA_MAPPER, 'ref_data', plant_destination)
        populate_xlxs(workbook, NEARESTPOINTS_MAPPER, 'nearest_points', plant_destination)
        workbook.close()
        return response
