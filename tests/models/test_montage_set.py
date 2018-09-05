import pytest
import django; django.setup()
from development.models import Chunk, RenderedVolume, Study, Specimen
from django.test.utils import override_settings
from development.models.montage_set import MontageSet
from django.utils.timezone import now
from development.models.camera import Camera
from development.models.microscope_type import MicroscopeType
from development.models.microscope import Microscope
from development.models.section import Section
from development.models.load import Load
from development.models.sample_holder import SampleHolder
from workflow_engine.models.configuration import Configuration


@pytest.fixture
def cameras_etc():
    camera, _ = \
        Camera.objects.update_or_create(
            uid='CAMERA_1',
            defaults={
                'height': 1234,
                'width': 1234,
                'model': 'MOCK_CAMERA'})

    scope_type, _ = \
        MicroscopeType.objects.update_or_create(
            name='MOCK MICROSCOPE TYPE')

    microscope, _ = \
        Microscope.objects.update_or_create(
            uid='MOCK MICROSCOPE',
            defaults={
                'microscope_type': scope_type
            })

    load, _ = Load.objects.update_or_create(
        uid='Mock Load',
        offset=1)

    z_mapping, _ = load.configurations.update_or_create(
        name='mock_z_mapping',
        configuration_type='z_mapping',
        defaults={
            'json_object': { "1": 2 } })

    sample_holder, _ = SampleHolder.objects.update_or_create(
        uid='Mock Sample Holder',
        defaults={
            'imaged_sections_count': 0,
            'load': load
        })

    return (camera, microscope, sample_holder)


@pytest.fixture
def section_factory():
    study, _ = Study.objects.update_or_create(
        name='MOCK STUDY'
    )

    specimen, _ = Specimen.objects.update_or_create(
        uid='MOCK SPECIMEN',
        defaults={
            'render_project': 'MOCK_PROJECT',
            'render_owner': 'MOCK_OWNER',
            'study': study
        })

    def factory(z_index):
        section = Section.objects.create(
            z_index=z_index,
            metadata=None,
            specimen=specimen)
        
        return section

    return factory

@pytest.fixture
def mock_tile_set(section_factory,
                  cameras_etc):
    storage_directory = '/path/to/storage_directory'
    metafile = '/path/to/metafile'
    (camera, microscope, sample_holder) = cameras_etc

    montage_set = MontageSet.objects.create(
        acquisition_date=now(),
        object_state='PENDING',
        section=section_factory(1),
        sample_holder=sample_holder,
        storage_directory=storage_directory,
        metafile=metafile,
        camera=camera,
        microscope=microscope)

    return montage_set

@pytest.mark.django_db
def test_get_section_index_queries(mock_tile_set):
    assert mock_tile_set.get_section_z_index() == 1
