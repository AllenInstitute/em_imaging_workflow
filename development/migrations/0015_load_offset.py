# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0014_montage_set_blank_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='offset',
            field=models.IntegerField(null=True),
        ),
    ]
