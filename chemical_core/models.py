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
        db_table = "chemical_preferences"
        verbose_name = "Chemical Preference"
        verbose_name_plural = "Chemical Preferences"
