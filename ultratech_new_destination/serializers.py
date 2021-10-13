from rest_framework.serializers import ModelSerializer

from ultratech_new_destination.models import Destination, PlantMapData, SimilarityData, RefData, NearestPoints, \
    MapAPIData


class DestinationSerializers(ModelSerializer):
    class Meta:
        model = Destination
        fields = ('source_lat,'
                  'source_long',
                  'new_destination_lat',
                  'new_destination_long',
                  'request_user')


class PlantMapDataSerializers(ModelSerializer):
    def create(self, validated_data):
        return PlantMapData.objects.create(**validated_data)

    class Meta:
        model = PlantMapData
        fields = (
            'plant_destination',
            'plant',
            'plant_name',
            'source_lat',
            'source_long',
            'destination_name',
            'new_destination_lat',
            'new_destination_long',
            'distance_source_newdestination',
            'ref_city_code1',
            'ref_city_code2',
            'ref_city_code1_latitude',
            'ref_city_code1_longitude',
            'ref_city_code2_latitude',
            'ref_city_code2_longitude',
            'nearest_greater_lat',
            'nearest_greater_long',
            'nearest_smaller_lat',
            'nearest_smaller_long',
            'lead_proposed',
            'optimum_ptpk',
            'optimum_base_freight',
            'ptpk_change_per_km',
            'lead_diff',
            'ptpk_diff_from_ref_city1',
            'similarity_predicted_ptpk'
        )


class SimilarityDataSerializers(ModelSerializer):
    def create(self, validated_data):
        return SimilarityData.objects.create(**validated_data)

    class Meta:
        model = SimilarityData
        fields = ('plant_destination',
                  'plant',
                  'city_code',
                  'truck_type',
                  'direct_sto',
                  'mean_ele',
                  'median_ele',
                  'max_ele',
                  'min_ele',
                  'range_ele',
                  'sd_ele',
                  'kurtosis_ele',
                  'skewness_ele',
                  'nh_per',
                  'sh_per',
                  'other_per',
                  'lead',
                  'ptpk',
                  'plain_per',
                  'hilly_per',
                  'slab',
                  'simi_predicted_ptpk')


class RefDataSerializer(ModelSerializer):
    def create(self, validated_data):
        return RefData.objects.create(**validated_data)

    class Meta:
        model = RefData
        fields = ('plant_destination',
                  'city_name',
                  'ptpk',
                  'lead',
                  'quantity',
                  'toll',
                  'unloading')


class NearestPointsSerializer(ModelSerializer):
    def create(self, validated_data):
        return NearestPoints.objects.create(**validated_data)

    class Meta:
        model = NearestPoints
        fields = ('plant_destination',
                  'city_name',
                  'taluka_name',
                  'lead',
                  'ptpk',
                  'google_dist',
                  'quantity',
                  'toll',
                  'unloading')


class MapAPIDataSerializer(ModelSerializer):
    class Meta:
        model = MapAPIData
        fields = ('plant_destination',
                  'geocode_latlong',
                  'distance_matrix',
                  'elev_url',
                  'elevation_extraction')
