from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hindalco.views import LITView
LIT_ROUTER = DefaultRouter()

LIT_ROUTER.register('lit', LITView, basename='LITView')

urlpatterns = [
    path('data/', include(LIT_ROUTER.urls)),
]