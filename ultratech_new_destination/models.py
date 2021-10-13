from django.db import models

from core.models import ModelBase
from django.contrib.postgres.fields import JSONField


class Destination(ModelBase):
    source_lat = models.FloatField(null=True, blank=True)
    source_long = models.FloatField(null=True, blank=True)
    new_destination_lat = models.FloatField(null=True, blank=True)
    new_destination_long = models.FloatField(null=True, blank=True)
    request_user = models.CharField(max_length=128, null=True, blank=True)
    truck_type = models.IntegerField(null=True, blank=True)
    taluka = models.CharField(max_length=128, null=True, blank=True)
    direct_sto = models.CharField(max_length=128, null=True, blank=True)
    similarity = models.FloatField(null=True, blank=True)


class PlantMapData(ModelBase):
    plant_destination = models.ForeignKey(Destination, related_name='map_data', on_delete=models.CASCADE)
    plant = models.IntegerField(null=False)
    plant_name = models.CharField(max_length=256, null=True, blank=True)
    source_lat = models.FloatField(null=True, blank=True)
    source_long = models.FloatField(null=True, blank=True)
    destination_name = models.CharField(max_length=256, null=True, blank=True)
    new_destination_lat = models.FloatField(null=True, blank=True)
    new_destination_long = models.FloatField(null=True, blank=True)
    distance_source_newdestination = models.FloatField(null=True, blank=True)
    ref_city_code1 = models.CharField(max_length=128, null=True, blank=True)
    ref_city_code2 = models.CharField(max_length=128, null=True, blank=True)
    ref_city_code1_latitude = models.FloatField(null=True, blank=True)
    ref_city_code1_longitude = models.FloatField(null=True, blank=True)
    ref_city_code2_latitude = models.FloatField(null=True, blank=True)
    ref_city_code2_longitude = models.FloatField(null=True, blank=True)
    nearest_greater_lat = models.FloatField(null=True, blank=True)
    nearest_greater_long = models.FloatField(null=True, blank=True)
    nearest_smaller_lat = models.FloatField(null=True, blank=True)
    nearest_smaller_long = models.FloatField(null=True, blank=True)
    lead_proposed = models.FloatField(null=True, blank=True)
    optimum_ptpk = models.FloatField(null=True, blank=True)
    optimum_base_freight = models.IntegerField(null=True, blank=True)
    ptpk_change_per_km = models.FloatField(null=True, blank=True)
    lead_diff = models.FloatField(null=True, blank=True)
    ptpk_diff_from_ref_city1 = models.FloatField(null=True, blank=True)
    similarity_predicted_ptpk = models.CharField(max_length=128, null=True, blank=True)
    comment = models.CharField(max_length=2048, null=True, blank=True)
    comment_lead = models.CharField(max_length=2048, null=True, blank=True)


class SimilarityData(ModelBase):
    plant_destination = models.ForeignKey(Destination, related_name='similarity_data', on_delete=models.CASCADE)
    plant = models.IntegerField(null=True, blank=True)
    city_code = models.CharField(max_length=128, null=True, blank=True)
    truck_type = models.IntegerField(null=True, blank=True)
    direct_sto = models.CharField(max_length=128, null=True, blank=True)
    mean_ele = models.FloatField(null=True, blank=True)
    median_ele = models.FloatField(null=True, blank=True)
    max_ele = models.FloatField(null=True, blank=True)
    min_ele = models.FloatField(null=True, blank=True)
    range_ele = models.FloatField(null=True, blank=True)
    sd_ele = models.FloatField(null=True, blank=True)
    kurtosis_ele = models.FloatField(null=True, blank=True)
    skewness_ele = models.FloatField(null=True, blank=True)
    nh_per = models.FloatField(null=True, blank=True)
    sh_per = models.FloatField(null=True, blank=True)
    other_per = models.FloatField(null=True, blank=True)
    lead = models.IntegerField(null=True, blank=True)
    ptpk = models.FloatField(null=True, blank=True)
    plain_per = models.FloatField(null=True, blank=True)
    hilly_per = models.FloatField(null=True, blank=True)
    slab = models.CharField(max_length=128, null=True, blank=True)
    simi_predicted_ptpk = models.FloatField(null=True, blank=True)
    similarity_values = models.CharField(max_length=128, null=True, blank=True)
    total_restriction_time = models.FloatField(null=True, blank=True)
    city_desc = models.CharField(max_length=128, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    i2_taluka_desc = models.CharField(max_length=128, null=True, blank=True)


class RefData(ModelBase):
    plant_destination = models.ForeignKey(Destination, related_name='ref_data', on_delete=models.CASCADE)
    city_name = models.CharField(max_length=128, null=True, blank=True)
    ptpk = models.FloatField(null=True, blank=True)
    lead = models.IntegerField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    toll = models.IntegerField(null=True, blank=True)
    unloading = models.IntegerField(null=True, blank=True)


class NearestPoints(ModelBase):
    plant_destination = models.ForeignKey(Destination, related_name='nearest_points', on_delete=models.CASCADE)
    city_name = models.CharField(max_length=128, null=True, blank=True)
    taluka_name = models.CharField(max_length=128, null=True, blank=True)
    lead = models.IntegerField(null=True, blank=True)
    ptpk = models.FloatField(null=True, blank=True)
    google_dist = models.IntegerField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    toll = models.IntegerField(null=True, blank=True)
    unloading = models.IntegerField(null=True, blank=True)


class MapAPIData(ModelBase):
    plant_destination = models.ForeignKey(Destination, related_name='map_api_data', on_delete=models.CASCADE)
    geocode_latlong = JSONField(default=dict, blank=True, null=True)
    distance_matrix = JSONField(default=dict, blank=True, null=True)
    elev_url = JSONField(default=dict, blank=True, null=True)
    elevation_extraction = JSONField(default=dict, blank=True, null=True)
    reverse_geocode = JSONField(default=dict, blank=True, null=True)
