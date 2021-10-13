from import_export import resources

from chemical_analysis.models import Chemical_Similarity_Data


class ProductSimiResource(resources.ModelResource):
    class Meta:
        model = Chemical_Similarity_Data

# class SimiResource(resources.ModelResource):
#     class Meta:
#         model = simi_data
