# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 20:53
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):
    initial=True

    dependencies = [
        ('at_em_imaging_workflow', '0017_remove_workflow_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunk',
            name='load',
            field=models.ForeignKey('Load',null=True, blank=True)
        ),
    ]