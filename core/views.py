# Create your views here.
import logging

from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from core.utils import update_password
from core.models import Preferences
from core.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from core.serializers import UserProfileSerializer
from django.contrib.auth import authenticate

LOGGER = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    View set for user
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        """
        permission defined specific to each user
        :return:
        """
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'delete':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['PUT'], url_name='change_password', url_path='change-password')
    def change_password(self, request):
        """
        function to update password of the user
        :param request:
        :return:
        """
        user = request.user
        old_password = request.data.get('old_password')
        if authenticate(username=user.username, password=old_password):
            new_password = request.data.get('new_password')
            update_password(user, new_password)
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['GET'], url_name='product/permission', url_path='product/permission')
    # def product_permission(self, request):
    #     """
    #     function returns the requested product allowed to be viewed by the user
    #     :param request:
    #     :return:
    #     """
    #     fare_products = list(Preferences.objects.filter(key="fare").
    #                          values('value'))[0]['value'].split(',')
    #     hil_products = list(Preferences.objects.filter(key="HIL").
    #                         values('value'))[0]['value'].split(',')
    #     main_product = list(Preferences.objects.filter(key="main_product").
    #                         values('value'))[0]['value'].split(',')
    #
    #     user = request.user
    #     LOGGER.info("User logged in : {}".format(user))
    #     # LOGGER.info("All permission given through group: {}".format(user.get_group_permissions()))
    #
    #     product_permission = list(user.groups.all().values('name'))
    #     LOGGER.info("user permission: {}".format(product_permission))
    #     response = list()
    #     prod_dict = dict()
    #     for each_prod in main_product:
    #         prod_dict[each_prod] = list()
    #     response.append(prod_dict)
    #     for each_product in product_permission:
    #         if each_product['name'] in fare_products:
    #             response[0]['fare'].append(each_product['name'])
    #         if each_product['name'] in hil_products:
    #             response[0]['HIL'].append(each_product['name'])
    #     return Response(response)

    @action(detail=False, methods=['GET'], url_name='product/permission', url_path='product/permission')
    def product_permission(self, request):
        """
            function returns the requested product allowed to be viewed by the user
            :param request:
            :return:
        """
        user = request.user
        LOGGER.info("User logged in : {}".format(user))
        product_permission = list(permission.get('name') for permission in list(user.groups.all().values('name')))
        LOGGER.info("user permission: {}".format(product_permission))
        return Response(data=product_permission)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'email or password is wrong'
    }


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer