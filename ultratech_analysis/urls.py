from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ultratech_analysis.views import SimilarityDataViewSet, NewSimilarityViewSet

SIMILARITY_ROUTER = DefaultRouter()

SIMILARITY_ROUTER.register('', SimilarityDataViewSet)
SIMILARITY_ROUTER.register('new', NewSimilarityViewSet)

urlpatterns = [
    
    path('data/', include(SIMILARITY_ROUTER.urls)),

]
