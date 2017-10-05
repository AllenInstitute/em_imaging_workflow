from django.db import models
from django.contrib.postgres.fields import JSONField
from workflow_engine.blue_sky_state_machine import BlueSkyStateMachine

class Study(models.Model):
    name = models.CharField(max_length=255, null=True)
    storage_directory = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Specimen(models.Model):
    uid = models.CharField(max_length=255, null=True)
    render_project = models.CharField(max_length=255, null=True)
    render_owner = models.CharField(max_length=255, null=True)
    study = models.ForeignKey(Study)

class RenderedVolumn(models.Model):
    mipmap_directory = models.CharField(max_length=255, null=True)
    specimen = models.ForeignKey(Specimen)

class Chuck(models.Model):
    size = models.IntegerField(null=True)
    chunk_state = models.CharField(max_length=255, null=True)
    rendered_volumn = models.ForeignKey(RenderedVolumn)
    preceding_chunk = models.ForeignKey('self', related_name='%(class)s_preceding_chunk')
    following_chunk = models.ForeignKey('self', related_name='%(class)s_following_chunk')

    def set_chuck_size(self):
        #TODO
        self.size = 0

    def is_complete(self):
        #TODO
        return True

class Load(models.Model):
    uid = models.CharField(max_length=255, null=True)

class SampleHolder(models.Model):
    uid = models.CharField(max_length=255, null=True)
    imaged_sections_count = models.IntegerField(null=True)
    load = models.ForeignKey(Load)

class Section(models.Model):
    section_id = models.CharField(max_length=255, null=True)
    z_index = models.IntegerField(null=True)
    metadata = JSONField(null=True)
    specimen = models.ForeignKey(Specimen)
    chucks = models.ManyToManyField(Chuck, related_name='sections')
    sample_holders = models.ManyToManyField(SampleHolder, related_name='sample_holders')

class Stain(models.Model):
    name = models.CharField(max_length=255, null=True)

class Camera(models.Model):
    uid = models.CharField(max_length=255, null=True)

class MicroscopeType(models.Model):
    name = models.CharField(max_length=255, null=True)

class Microscope(models.Model):
    uid = models.CharField(max_length=255, null=True)
    microscope_type = models.ForeignKey(MicroscopeType)

class TileImageSet(models.Model):
    storage_directory = models.CharField(max_length=255, null=True)
    workflow_state = models.CharField(max_length=255, null=True)
    camera = models.ForeignKey(Camera, null=True)
    microscope = models.ForeignKey(Microscope, null=True)

class MontageSet(TileImageSet):
    uid = models.CharField(max_length=255, null=True)
    acquisition_date = models.DateTimeField(null=True)
    mipmap_directory = models.CharField(max_length=255, null=True)
    section = models.ForeignKey(Section)
    sample_holder = models.ForeignKey(SampleHolder)

class ReferenceSet(TileImageSet):
    uid = models.CharField(max_length=255, null=True)
    project_path = models.CharField(max_length=255)

class EMMontageSet(MontageSet):
    reference_set = models.ForeignKey(ReferenceSet)
    reference_set_uid = models.CharField(max_length=255, null=True)

class RegistrationSeries(models.Model):
    size = models.IntegerField(null=True)
    workflow_state = models.CharField(max_length=255, null=True)

    def is_complete(self):
        #TODO
        return True

    def get_reference_state(self):
        #TODO
        return 'TODO'

class ATMontageSet(MontageSet):
    image_session_number = models.CharField(max_length=255, null=True)
    registration_series = models.ForeignKey(RegistrationSeries)

    def has_z_index(self):
        return True
