from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chemical_analysis.views import ChemicalDataViewSet

CHEMICAL_ROUTER = DefaultRouter()

CHEMICAL_ROUTER.register('', ChemicalDataViewSet)

urlpatterns = [

    path('data/', include(CHEMICAL_ROUTER.urls)),

]
