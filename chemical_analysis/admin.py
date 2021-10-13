from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from chemical_analysis.models import Chemical_Similarity_Data
from chemical_core.admin import ChemicalsDBModelAdmin


@admin.register(Chemical_Similarity_Data)
class ProductSimilarityDataAdmin(ImportExportModelAdmin, ChemicalsDBModelAdmin):
    """
    Admin customization for Historical Data
    """
    list_display = [field.name for field in Chemical_Similarity_Data._meta.get_fields()]
    search_fields = [field.name for field in Chemical_Similarity_Data._meta.get_fields()]


