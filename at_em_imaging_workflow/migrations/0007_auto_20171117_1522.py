# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-17 23:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('at_em_imaging_workflow', '0006_auto_20171111_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emmontageset',
            name='reference_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='at_em_imaging_workflow.ReferenceSet'),
        ),
    ]
