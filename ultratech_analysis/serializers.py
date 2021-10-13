from rest_framework import serializers

from ultratech_analysis.models import simi_data, SimilarityData


class SimilarityDataSerializer(serializers.ModelSerializer):
    """
    Serializer class for similarity data set
    """

    class Meta:
        """
        fields customization for similarity data set
        """
        model = simi_data
        exclude = ('id',)


class NewSimilarityDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimilarityData
        exclude = ('id',)
