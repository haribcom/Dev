from django.contrib import admin

# Register your models here.
from django.db import transaction
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from ultratech_analysis.constants import SIMILARITY_DATA_MAPPER
from ultratech_analysis.models import simi_data, SimilarityData
from ultratech_core.admin import UltraTechDBModelAdmin


class SimilarityDataResource(resources.ModelResource):
    class Meta:
        model = SimilarityData

    def before_import_row(self, row, **kwargs):
        try:
            with transaction.atomic():
               # row['plant'] = row['plant_code']
               # row = {SIMILARITY_DATA_MAPPER.get(db_row_name): row.get(db_row_name) for db_row_name in SIMILARITY_DATA_MAPPER.keys()}
               for db_row_name in SIMILARITY_DATA_MAPPER.keys():
                   row[SIMILARITY_DATA_MAPPER.get(db_row_name)] = row.get(db_row_name)
        except:
            pass


@admin.register(SimilarityData)
class SimilarityDataAdmin(ImportExportModelAdmin, UltraTechDBModelAdmin):
    """
    Admin customization for Historical Data
    """
    list_display = [field.name for field in SimilarityData._meta.get_fields()]
    search_fields = [field.name for field in SimilarityData._meta.get_fields()]
    resource_class = SimilarityDataResource








