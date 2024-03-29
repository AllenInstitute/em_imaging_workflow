# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-04 00:20
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('at_em_imaging_workflow', '0019_load_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chunk',
            name='chunk_state',
        ),
        migrations.AddField(
            model_name='chunkassignment',
            name='object_state',
            field=django_fsm.FSMField(default='PENDING', max_length=50),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='object_state',
            field=django_fsm.FSMField(default='PENDING', max_length=50),
        ),
    ]
