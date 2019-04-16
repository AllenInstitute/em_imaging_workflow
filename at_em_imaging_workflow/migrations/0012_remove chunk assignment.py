# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('at_em_imaging_workflow', '0011_chunk_computed_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='chunks',
        ),
        migrations.AlterField(
            model_name='chunk',
            name='following_chunk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chunk_following_chunk', to='at_em_imaging_workflow.Chunk'),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='preceding_chunk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chunk_preceding_chunk', to='at_em_imaging_workflow.Chunk'),
        ),
    ]