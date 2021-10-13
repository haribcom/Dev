# Generated by Django 3.0.6 on 2020-07-24 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultratech_new_destination', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nearestpoints',
            old_name='base_freight',
            new_name='google_dist',
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='destination_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='lead_diff',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='nearest_greater_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='nearest_greater_long',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='nearest_smaller_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='nearest_smaller_long',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='plant_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='ptpk_change_per_km',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plantmapdata',
            name='ptpk_diff_from_ref_city1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='city_code',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='direct_sto',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='hilly_per',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='nh_per',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='other_per',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='plain_per',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='plant',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='sh_per',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='slab',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='refdata',
            name='truck_type',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]