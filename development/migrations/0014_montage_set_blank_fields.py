# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-17 02:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0013_chunk assignment join through table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emmontageset',
            name='reference_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='development.ReferenceSet'),
        ),
        migrations.AlterField(
            model_name='emmontageset',
            name='reference_set_uid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
