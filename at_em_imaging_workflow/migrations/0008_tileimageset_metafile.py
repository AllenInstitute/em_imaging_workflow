# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-22 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('at_em_imaging_workflow', '0007_auto_20171117_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='tileimageset',
            name='metafile',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
