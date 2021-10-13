from django.urls import path, include
from rest_framework import routers
from ultratech_new_destination.views import DestinationView

router = routers.DefaultRouter()
router.register('', DestinationView)

urlpatterns = [
    path(r'', include(router.urls))
]
