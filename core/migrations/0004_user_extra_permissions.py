# Generated by Django 3.0.6 on 2020-08-12 17:51

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='extra_permissions',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]
