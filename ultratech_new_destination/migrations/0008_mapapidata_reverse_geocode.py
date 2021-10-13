# Generated by Django 3.0.6 on 2020-08-12 14:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultratech_new_destination', '0007_auto_20200812_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapapidata',
            name='reverse_geocode',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]
