# Generated by Django 3.0.6 on 2020-09-07 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ultratech_new_destination', '0009_plantmapdata_comment_lead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantmapdata',
            name='comment',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
