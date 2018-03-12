# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-15 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0009_referenceset_manifest_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='montageset',
            name='acquisition_date',
        ),
        migrations.AddField(
            model_name='tileimageset',
            name='acquisition_date',
            field=models.DateTimeField(null=True),
        ),
    ]