from rest_framework.permissions import DjangoModelPermissions


class ModelPermissions(DjangoModelPermissions):
    """
    Only models having this permission will be able to perform any operations.
    """

    def __init__(self, *args, **kwargs):
        super(ModelPermissions, self).__init__()
        self.perms_map.update({'GET': ['%(app_label)s.view_%(model_name)s']})
