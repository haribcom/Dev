from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', include('core.urls')),
    path('simi/', include('ultratech_analysis.urls')),
    path('chemicals/', include('chemical_analysis.urls')),
    path('admin/', admin.site.urls),
    path('new-destination/', include('ultratech_new_destination.urls')),
    path('hindalco/', include('hindalco.urls'))
]
