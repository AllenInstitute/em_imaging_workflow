# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-07 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('at_em_imaging_workflow', '0003_auto_20171107_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='montageset',
            name='overlap',
            field=models.FloatField(null=True),
        ),
    ]
