from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField


# Create your models here.
# Customize the default user model, by inheriting AbstractUser model


class User(AbstractUser):
    """
    Abstract model for User.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_('email_address'), unique=True)
    USERNAME_FIELD = 'email'
    extra_permissions = JSONField(default=dict, blank=True, null=True)

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


class ModelBase(models.Model):
    """
    Base model for every class which will have created_on and updated_at
    """
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for base model which will be uploaded throughout.
        """
        abstract = True


class Product(ModelBase):
    """
    Model which handle all the product
    """
    product_name = models.CharField(max_length=50, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}".format(self.product_name)

    class Meta:
        db_table = "product"
        verbose_name = "Products"
        verbose_name_plural = "Products"


class AbstractPreferences(ModelBase):
    """
    Preferences table to store assumed constant which may change in future.
    """
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=10000)
    description = models.TextField()

    def __str__(self):
        return self.key

    class Meta:
        """
        Customized db name for preferences has been provided.
        """
        abstract = True


class Preferences(AbstractPreferences):
    pass

    class Meta:
        db_table = "Preferences"
        verbose_name = "Main Preference"
        verbose_name_plural = "Main Preferences"
