import pytest
from at_em_imaging_workflow.models import (
    Camera,
    ChunkCalculator,
    EMMontageSet,
    Load,
    Microscope,
    MicroscopeType,
    MontageSet,
    RenderedVolume,
    SampleHolder, 
    Section,
    Specimen,
    Study
)
from django.utils import timezone
from django.utils.timezone import datetime
from django.utils.timezone import now
from datetime import timedelta
import pytz

_MOCK_LOAD_OFFSET = 10000
_MOCK_LOAD_SIZE = 3000
_MOCK_CHUNK_SIZE = 1000

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

    volume, _ = RenderedVolume.objects.update_or_create(
        mipmap_directory='/path/to/mipmap/directory',
        defaults={
            'specimen': specimen
        }
    )

    def factory(z_index):
        section = Section.objects.create(
            z_index=z_index + _MOCK_LOAD_OFFSET,
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
            'json_object': {
                str(n + _MOCK_LOAD_OFFSET): n for n in range(0, _MOCK_LOAD_SIZE)
            }
        }
    )

    sample_holder, _ = SampleHolder.objects.update_or_create(
        uid='Mock Sample Holder',
        defaults={
            'imaged_sections_count': 0,
            'load': load
        })

    return (camera, microscope, sample_holder)


@pytest.fixture
def lots_of_montage_sets(section_factory,
                         cameras_etc):
    overlap = 5
    storage_directory = '/path/to/storage_directory'
    metafile = '/path/to/metafile'
    (camera, microscope, sample_holder) = cameras_etc

    montage_sets = []

    timezone.activate(pytz.timezone('US/Pacific'))

    for i in range(0,_MOCK_CHUNK_SIZE):
        em_montage_set = EMMontageSet.objects.create(
            uid="Montage Set %d" %(i),
            acquisition_date=datetime(
                2345, 6, 7,
                8, 9, 10) + timedelta(seconds=i-1),
            overlap=overlap,
            object_state='PENDING',
            mipmap_directory=None,
            section=section_factory(i),
            sample_holder=sample_holder,
            reference_set=None,
            reference_set_uid='MOCK_REFERENCE_SET_UID',
            storage_directory=storage_directory,
            metafile=metafile,
            camera=camera,
            microscope=microscope)

        montage_sets.append(em_montage_set)

    return montage_sets


@pytest.fixture
def lots_of_chunks(lots_of_montage_sets):
    montage_sets = lots_of_montage_sets
    chunk_set = []

    load_object = montage_sets[0].get_load()
    volume_object = montage_sets[0].specimen().renderedvolume_set.first()

    computed_index = 900
    chunk_offset = 10000
    chunk_size = 100
    chunk_overlap = 10 # TODO: use % 16

    preceding_chunk = None

    while chunk_offset + chunk_size < 13000:
        chnk = ChunkCalculator.create_chunk(
            load_object,
            computed_index,
            chunk_offset,
            chunk_offset + chunk_size,
            volume_object
        )

        chnk.configurations.update_or_create(
            name='Rough Tile Pair Files {}'.format(computed_index),
            configuration_type='rough_tile_pair_file',
            defaults={
                'json_object': {
                    str(i): { 'tile_pair_file': '/rough/tile/pair/file' }
                    for i in range(chunk_offset, chunk_offset + chunk_size + 1)
                }
            }
        )

        chnk.configurations.update_or_create(
            name='Fusion Transform {}'.format(computed_index),
            configuration_type='fusion_transform',
            defaults={
                'json_object': {
                    'transform': {
                        'type': 'leaf',
                        'className': 'lorem.ipsum.Ipsum',
                        'dataString': "9.8 7.6 5.4 3.2 1.0"
                    }
                }
            }
        )

        if preceding_chunk:
            chnk.preceding_chunk = preceding_chunk
            chnk.save()
            preceding_chunk.following_chunk = chnk
            chnk.save()

        chunk_set.append(chnk)

        computed_index = computed_index + 1
        chunk_offset = chunk_offset + chunk_size - chunk_overlap
        preceding_chunk = chnk

    return chunk_set
