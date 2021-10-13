import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from chemical_analysis.controller import chemicals_drop_down, \
    chemicals_display, product_dd, product_plant_dd, product_plant_dest_dd
from chemical_analysis.models import Chemical_Similarity_Data
from chemical_analysis.serializers import ProductChemicalDataSerializer
from chemical_analysis.utils import list_of_similarity_field, route, add_location_graph
from core.utils import access_permissions
from master.permissions import ModelPermissions

LOGGER = logging.getLogger(__name__)


class ChemicalDataViewSet(viewsets.ModelViewSet):
    """
    Viewset for similarity data for chemicals
    """
    serializer_class = ProductChemicalDataSerializer
    queryset = Chemical_Similarity_Data.objects.all()
    permission_classes = (ModelPermissions,)
    lookup_field = 'type'

    @access_permissions(('chemicals',))
    @action(detail=False, methods=['GET'], url_name='query', url_path='query')
    def list_down(self, request):
        """
        This fn returns all the categories selection for pop up
        :param request:
        :return:
        """
        response = chemicals_drop_down()
        return Response(response)

    @access_permissions(('chemicals',))
    @action(detail=False, methods=['GET'], url_name='path-plant-product', url_path='product/plant/path')
    def path_sel_display(self, request):
        """
        the fn returns the corresponding details based on the path selected
        :param request:
        :return:
        """
        try:
            response = chemicals_display(path=request.GET['path'],
                                         plant=request.GET['plant'],
                                         product=request.GET['product'],
                                         destination=request.GET['destination'])
            if response:
                return Response(response)
            else:
                return Response({"message": "It is not possible to reach {} plant following {} path"
                                            " for {} product. "
                                            "Please select other combination.".
                                format(request.GET['plant'], request.GET['path'], request.GET['product'])},
                                status=HTTP_400_BAD_REQUEST)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api for chemicals %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please sent path, plant and product as body"},
                            status=HTTP_400_BAD_REQUEST)

    @access_permissions(('chemicals',))
    @action(detail=False, methods=['GET'], url_name='product', url_path='product/dd')
    def product_drop_down(self, request):
        """
        API to get the drop down based on the product
        :param request:
        :return:
        """
        try:
            res = product_dd(request.GET['product'])
            return Response(res)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please send product as param"},
                            status=HTTP_400_BAD_REQUEST)

    @access_permissions(('chemicals',))
    @action(detail=False, methods=['GET'], url_name='product-plant', url_path='product/plant/dd')
    def product_plant_dd(self, request):
        """
        API to get the drop down based on the product and plant
        :param request:
        :return:
        """
        try:
            res = product_plant_dd(request.GET['product'], request.GET['plant'])
            return Response(res)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please send product as param"},
                            status=HTTP_400_BAD_REQUEST)

    @access_permissions(('chemicals',))
    @action(detail=False, methods=['GET'], url_name='product-plant-dest', url_path='product/plant/dest/dd')
    def product_plant_dest_dd(self, request):
        """
        API to get the drop down based on the product and plant and destination
        :param request:
        :return:
        """
        try:
            toll = request.GET['toll'].capitalize()
            res = product_plant_dest_dd(request.GET['product'], request.GET['plant'], request.GET['destination'],
                                        toll)
            if res == 400:
                return Response({"message": "There is no path possible from selected filter. Please select app filter"},
                                status=HTTP_400_BAD_REQUEST)
            return Response(res)
        except KeyError as key_error:
            LOGGER.error("Error, key not sent while accessing api %s", key_error, exc_info=True)
            return Response({"message": "Missing key. Please send product as param"},
                            status=HTTP_400_BAD_REQUEST)
