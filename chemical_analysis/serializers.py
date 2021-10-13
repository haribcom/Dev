from rest_framework import serializers

from chemical_analysis.models import Chemical_Similarity_Data


# class ChemicalDataSerializer(serializers.ModelSerializer):
#     """
#     Serializer class for similarity data set
#     """
#
#     class Meta:
#         """
#         fields customization for similarity data set
#         """
#         model = simi_data
#         exclude = ('id',)


class ProductChemicalDataSerializer(serializers.ModelSerializer):
    """
    Serializer class for similarity data set
    """

    class Meta:
        """
        fields customization for similarity data set
        """
        model = Chemical_Similarity_Data
        exclude = ('id',)
