# Generated by Django 3.0.6 on 2020-05-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chemical_Similarity_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant', models.FloatField(null=True)),
                ('type', models.CharField(max_length=50, null=True)),
                ('city_code', models.CharField(max_length=50, null=True)),
                ('city_desc', models.CharField(max_length=100, null=True)),
                ('simi_type', models.CharField(max_length=100, null=True)),
                ('simi_city_code', models.CharField(max_length=50, null=True)),
                ('simi_city_name', models.CharField(max_length=100, null=True)),
                ('truck_type', models.CharField(max_length=50, null=True)),
                ('direct_sto', models.CharField(max_length=100, null=True)),
                ('mean_route_time_taken', models.FloatField(null=True)),
                ('mean_ele', models.FloatField(null=True)),
                ('sd_ele', models.FloatField(null=True)),
                ('nh_per', models.FloatField(null=True)),
                ('sh_per', models.FloatField(null=True)),
                ('other_per', models.FloatField(null=True)),
                ('lead', models.FloatField(null=True)),
                ('ptpk', models.FloatField(null=True)),
                ('plain_per', models.FloatField(null=True)),
                ('hilly_per', models.FloatField(null=True)),
                ('onward_travel', models.FloatField(null=True)),
                ('return_travel', models.FloatField(null=True)),
                ('idle_time_cust', models.FloatField(null=True)),
                ('slab', models.CharField(max_length=50, null=True)),
                ('city_no', models.CharField(max_length=50, null=True)),
                ('simi_coeff', models.FloatField(null=True)),
                ('path', models.CharField(max_length=50, null=True)),
                ('ptpk_pred', models.FloatField(null=True)),
                ('quantity', models.FloatField(null=True)),
                ('batch', models.CharField(max_length=100, null=True)),
                ('source_lat', models.FloatField(null=True)),
                ('source_long', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('pred_base_freight', models.FloatField(null=True)),
                ('impact', models.FloatField(null=True)),
                ('base_freight', models.FloatField(null=True)),
                ('taluka', models.CharField(max_length=100, null=True)),
                ('i2_taluka_desc', models.CharField(max_length=100, null=True)),
                ('t_type', models.CharField(max_length=100, null=True)),
                ('full_plant_name', models.CharField(max_length=100, null=True)),
                ('simi_city', models.CharField(max_length=100, null=True)),
                ('full_city', models.CharField(max_length=100, null=True)),
                ('route_1', models.CharField(max_length=200, null=True)),
                ('route', models.CharField(max_length=200, null=True)),
                ('route_2', models.CharField(max_length=200, null=True)),
                ('plant_name', models.CharField(max_length=200, null=True)),
                ('simi_route', models.CharField(max_length=200, null=True)),
                ('product', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Chemicals Similarity Data Product',
                'verbose_name_plural': 'Chemicals Similarity Data Product',
                'db_table': 'simi_data_chemicals',
            },
        ),
        migrations.CreateModel(
            name='simi_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, null=True)),
                ('plant', models.FloatField(null=True)),
                ('city_code', models.CharField(max_length=50, null=True)),
                ('truck_type', models.CharField(max_length=50, null=True)),
                ('direct_sto', models.CharField(max_length=50, null=True)),
                ('slab', models.FloatField(null=True)),
                ('mean_route_timetaken', models.FloatField(null=True)),
                ('mean_ele', models.FloatField(null=True)),
                ('median_ele', models.FloatField(null=True)),
                ('max_ele', models.FloatField(null=True)),
                ('min_ele', models.FloatField(null=True)),
                ('range_ele', models.FloatField(null=True)),
                ('sd_ele', models.FloatField(null=True)),
                ('kurtosis_ele', models.FloatField(null=True)),
                ('skewness_ele', models.FloatField(null=True)),
                ('nh_perc', models.FloatField(null=True)),
                ('sh_perc', models.FloatField(null=True)),
                ('other_perc', models.FloatField(null=True)),
                ('lead', models.FloatField(null=True)),
                ('ptpk', models.FloatField(null=True)),
                ('plain_perc', models.FloatField(null=True)),
                ('hilly_perc', models.FloatField(null=True)),
                ('onward_travel', models.FloatField(null=True)),
                ('route', models.CharField(max_length=100, null=True)),
                ('chc', models.FloatField(null=True)),
                ('simi_coeff', models.FloatField(null=True)),
                ('path_or_suggestion', models.CharField(max_length=100, null=True)),
                ('ptpk_pred', models.FloatField(null=True)),
                ('invoiced_qty', models.FloatField(null=True)),
                ('distance', models.FloatField(null=True)),
                ('org_freight_cost', models.FloatField(null=True)),
                ('changed_freight_cost', models.FloatField(null=True)),
                ('impact', models.FloatField(null=True)),
                ('source_lat', models.FloatField(null=True)),
                ('source_long', models.FloatField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('state_dec', models.CharField(max_length=100, null=True)),
                ('district_desc', models.CharField(max_length=100, null=True)),
                ('i2_taluka', models.CharField(max_length=100, null=True)),
                ('i2_taluka_desc', models.CharField(max_length=100, null=True)),
                ('city_desc', models.CharField(max_length=100, null=True)),
                ('base_freight', models.FloatField(null=True)),
                ('toll_rate', models.FloatField(null=True)),
            ],
            options={
                'verbose_name': 'Chemicals Similarity Data',
                'verbose_name_plural': 'Chemicals Similarity Data',
                'db_table': 'simi_data',
            },
        ),
    ]