from django.contrib import admin

# Register your models here.
from ultratech_new_destination.models import Destination, PlantMapData, SimilarityData, RefData, NearestPoints, \
    MapAPIData


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('source_lat', 'source_long', 'new_destination_lat', 'new_destination_long')


@admin.register(PlantMapData)
class PlantMapDataAdmin(admin.ModelAdmin):
    list_display = ("plant", "source_lat", "source_long", "plant_destination")


@admin.register(SimilarityData)
class SimilarityDataAdmin(admin.ModelAdmin):
    list_display = ("plant_destination", "plant", "city_code")


@admin.register(RefData)
class RefDataAdmin(admin.ModelAdmin):
    list_display = ("plant_destination", "city_name")


@admin.register(NearestPoints)
class NearestPointsAdmin(admin.ModelAdmin):
    list_display = ("plant_destination", "city_name")


@admin.register(MapAPIData)
class MapAPIDataAdmin(admin.ModelAdmin):
    list_display = ('plant_destination',
                    'geocode_latlong',
                    'distance_matrix',
                    'elev_url',
                    'elevation_extraction')
