from django.contrib import admin

# Register your models here.
from django import forms
from import_export.admin import ImportExportModelAdmin

from core.models import User, Product, Preferences


# code to show ModelMultipleChoiceField so that it can be used to extra permission keys like utcl_plants
# class UserForm(forms.ModelForm):
#     utcl_plants = forms.ModelMultipleChoiceField(queryset=User.objects.all())
#
#     class Meta:
#         model = User
#         fields = [field.name for field in User._meta.fields if field.name != "id"]
#         fields.append('utcl_plants')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    # form = UserForm
    # code to show save utcl plants ModelMultipleChoiceField in extra_permissions need to be tested
    # fields = [field.name for field in User._meta.fields if field.name != "id"]
    # def save_model(self, request, obj, form, change):
    #     utcl_plants = request.FILES.get('utcl_plants', None)
    #     if utcl_plants:
    #         obj.extra_permissions['utcl_plants'] = utcl_plants
    pass


class UserDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'admin'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


admin.site.register(Product, UserDBModelAdmin)


class PreferencesAdmin(ImportExportModelAdmin, UserDBModelAdmin):
    """
    To customize Preferences admin panel
    """
    list_display = ("id", "key", "value", "description",)
    list_editable = ("value", "description",)


admin.site.register(Preferences, PreferencesAdmin)
