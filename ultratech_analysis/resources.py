from import_export import resources

from ultratech_analysis.models import simi_data


class SimiResource(resources.ModelResource):
    class Meta:
        model = simi_data