import datetime
import logging
import re
from functools import reduce

from dateutil.relativedelta import relativedelta
from django.core.exceptions import FieldError
from django.db.models import F, Avg, Q
from django.shortcuts import render

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from core.error_response import FORBIDDEN_RESPONSE
from core.utils import access_permissions
from ultratech_analysis.constants import CURRENT_MONTH_FILTER, LAST_MONTH_FILTER, RED, GREEN, LIT_SOURCE, \
    LAST_MONTH_TILL_END_FILTER
from ultratech_analysis.controller import drop_down, plant_path_query, plant_dd, plant_taluka_dd, plant_taluka_cc_dd, \
    plant_taluka_cc_tt_dd
from ultratech_analysis.models import simi_data, SimilarityData
from ultratech_analysis.serializers import SimilarityDataSerializer, NewSimilarityDataSerializer
from master.permissions import ModelPermissions
from ultratech_analysis.utils import format_filter_response, format_dashboard_response
from ultratech_new_destination.utils import check_plant_access, get_allowed_plants


from utils import populate_xlxs_from_queryset

LOGGER = logging.getLogger('django')


class SimilarityDataViewSet(viewsets.ModelViewSet):
    """
    Viewset for similarity data
    """
    serializer_class = SimilarityDataSerializer
    queryset = simi_data.objects.all()
    permission_classes = (ModelPermissions,)
    lookup_field = 'Role_ID'

    @action(detail=False, methods=['GET'], url_name='query', url_path='query')
    def query(self, request):
        """
        To insert the data in manual forecast table
        and store it local path.
        :param request:
        :return:
        """
        response = drop_down()
        return Response(response)

    @action(detail=False, methods=['GET'], url_name='path-plant', url_path='plant/path')
    def path_selected_on_plant(self, request):
        """
        This API will give all the other details of static dashboard based on the path selected
        :return:
        """
        try:
            res, status = plant_path_query(int(request.GET['plant']), request.GET['path'],
                                           request.GET['taluka'], request.GET['city_code'],
                                           request.GET['truck_type'])
            if status == 200:
                return Response(res)
            elif status == 400:
                return Response(res, status=HTTP_400_BAD_REQUEST)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please send path and plant as param"},
                            status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_name='plant', url_path='plant')
    def plant_drop_down(self, request):
        """
        API to get the drop down based on the path
        :param request:
        :return:
        """
        try:
            res, status = plant_dd(request.GET['plant'])
            if status == 200:
                return Response(res)
            elif status == 400:
                return Response(res, status=HTTP_400_BAD_REQUEST)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please send plant as param"},
                            status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_name='plant-taluka', url_path='plant/taluka')
    def plant_taluka_drop_down(self, request):
        """
        API to get the drop down based on the path
        :param request:
        :return:
        """
        try:
            res, status = plant_taluka_dd(request.GET['plant'], request.GET['taluka'])
            if status == 200:
                return Response(res)
            elif status == 400:
                return Response(res, status=HTTP_400_BAD_REQUEST)
            # return Response(res)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please send plant as param"},
                            status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_name='plant-taluka-cc', url_path='plant/taluka/city-code')
    def plant_taluka_cc_drop_down(self, request):
        """
        API to get the drop down based on the path
        :param request:
        :return:
        """
        try:
            res, status = plant_taluka_cc_dd(request.GET['plant'], request.GET['taluka'], request.GET['city_code'])
            # return Response(res)
            if status == 200:
                return Response(res)
            elif status == 400:
                return Response(res, status=HTTP_400_BAD_REQUEST)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please send plant as param"},
                            status=HTTP_400_BAD_REQUEST) @ action(detail=False, methods=['GET'],
                                                                  url_name='plant-taluka-cc',
                                                                  url_path='plant/taluka/city-code')

    @action(detail=False, methods=['GET'], url_name='plant-taluka-cc', url_path='plant/taluka/city-code/truck-type')
    def plant_taluka_cc_tt_drop_down(self, request):
        """
        API to get the drop down based on the path
        :param request:
        :return:
        """
        try:
            res, status = plant_taluka_cc_tt_dd(request.GET['plant'], request.GET['taluka'],
                                                request.GET['city_code'], request.GET['truck_type'])
            # return Response(res)
            if status == 200:
                return Response(res)
            elif status == 400:
                return Response(res, status=HTTP_400_BAD_REQUEST)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please send plant as param"},
                            status=HTTP_400_BAD_REQUEST)


class NewSimilarityViewSet(viewsets.ModelViewSet):
    queryset = SimilarityData.objects.all()
    serializer_class = NewSimilarityDataSerializer
    # permission_classes = [AllowAny]

    @access_permissions(('ultratech',))
    @action(detail=False, methods=['GET'], url_name='filter', url_path='filter')
    def filter(self, request):
        """
        api to send data for filters
        :param request:
        :return:
        """
        filters = dict()
        for param in request.GET.keys():
            filters[param] = request.GET[param]
        plant = request.GET.get('plant')
        if plant:
            plant_code = plant.split('-')[0]
            filters['plant'] = plant_code
        if filters.get('city'):
            filters['city_code'] = filters['city'].split('-')[0]
            filters.pop('city')
        if plant and not check_plant_access(request.user, plant_code):  # checking user have requested plant access
            return Response(status=HTTP_403_FORBIDDEN, data=FORBIDDEN_RESPONSE.get("PLANT_ACCESS_DENIED"))
        elif not plant:
            filters['plant__in'] = get_allowed_plants(request.user)
        try:
            data = self.queryset.filter(**filters).values('plant', 'plant_name', 'truck_type', 'i2_taluka_desc',
                                                          'city_code', 'city_desc')
        except (FieldError, ValueError) as ex:
            LOGGER.exception("Exception in ultratech Similarity analysis filter while making query")
            return Response(data='wrong parameters')
        data = format_filter_response(data)  # parse data into the required format
        if not data.get('plant'):
            return Response(status=HTTP_403_FORBIDDEN, data=FORBIDDEN_RESPONSE.get('NO_PLANT_ACCESS'))
        return Response(data=data)

    @access_permissions(('ultratech',))
    @action(detail=False, methods=['GET'], url_name='dashboard', url_path='dashboard')
    def dashboard(self, request):
        """
        return data to show on dashboard
        :param request:
        :return:
        """
        filters = dict()
        plant = request.GET.get('plant')
        plant_code = plant.split('-')[0]
        if not check_plant_access(request.user, plant_code):  # checking user have requested plant access
            return Response(status=HTTP_403_FORBIDDEN, data=FORBIDDEN_RESPONSE.get("PLANT_ACCESS_DENIED"))
        for param in request.GET.keys():
            filters[param] = request.GET[param]
        if plant:
            filters['plant'] = plant_code
        if filters.get('city'):
            filters['city_code'] = filters['city'].split('-')[0]
            filters.pop('city')
        try:
            data = self.queryset.filter(**filters).order_by('-simi_coeff')[:5]  # Todo: add values
            current_data = SimilarityData.objects.filter(**filters, simi_coeff=1)
            filters.pop('city_code', None)
            route_data = SimilarityData.objects.filter(**filters, path="Path").order_by('impact')
        except (FieldError, ValueError) as ex:
            LOGGER.exception("Exception in ultratech Similarity analysis dashboard while making query")
            return Response(data='wrong parameters')
        data = format_dashboard_response(data, current_data.first(), route_data)  # parse data into the required format
        return Response(data=data)

    @access_permissions(('ultratech',))
    @action(detail=False, methods=['GET'], url_name='download', url_path='download')
    def download(self, request, *args, **kwargs):
        filters = dict()
        plant = request.GET.get('plant')

        if not plant:
            filters['plant__in'] = request.user.extra_permissions.get('utcl_plants')
        else:
            plant_code = plant.split('-')[0]
            if not check_plant_access(request.user, plant_code):  # checking user have requested plant access
                return Response(status=HTTP_403_FORBIDDEN, data=FORBIDDEN_RESPONSE.get("PLANT_ACCESS_DENIED"))
            for param in request.GET.keys():
                if request.GET[param]:
                    filters[param] = request.GET[param]
            if plant:
                filters['plant'] = plant_code
            if filters.get('city'):
                filters['city_code'] = filters['city'].split('-')[0]
                filters.pop('city')
        try:
            data = self.queryset.filter(**filters).order_by('-simi_coeff')
        except (FieldError, ValueError) as ex:
            LOGGER.exception("Exception in ultratech Similarity analysis dashboard while making query")
            return Response(data='wrong parameters')
        return populate_xlxs_from_queryset(SimilarityData, data, "similarity")
