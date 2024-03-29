# Generated by Django 2.2 on 2020-01-31 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('at_em_imaging_workflow', '0020_object_state_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='montageset',
            name='mipmap_directory',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='referenceset',
            name='manifest_path',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='referenceset',
            name='project_path',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='renderedvolume',
            name='mipmap_directory',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='storage_directory',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='tileimageset',
            name='metafile',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='tileimageset',
            name='storage_directory',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
