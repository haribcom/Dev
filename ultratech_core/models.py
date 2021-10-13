from django.db import models


# Create your models here.
from core.models import AbstractPreferences


class Preferences(AbstractPreferences):
    """
    Preferences table to store assumed constant which may change in future.
    """
    pass

    class Meta:
        """
        Customized db name for preferences has been provided.
        """
        db_table = "ultra_tech_preferences"
        verbose_name = "Ultra Tech Preference"
        verbose_name_plural = "Ultra Tech Preferences"
