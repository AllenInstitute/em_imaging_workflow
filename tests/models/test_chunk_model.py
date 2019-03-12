import pytest
import django; django.setup()
from django.conf import settings
from development.models import Chunk, RenderedVolume, Study, Specimen
from django.test.utils import override_settings
from development.models.e_m_montage_set import EMMontageSet
from django.utils import timezone
from django.utils.timezone import datetime
from tests.models.test_montage_set import cameras_etc, section_factory
from datetime import timedelta
import pytz

def test_str():
    study = Study(
        name="Lorem Ipsum",
        storage_directory="/Lorem/ipsum/dolor/sit/amet/consectetur")
    specimen = Specimen(
        uid="DEADBEEF",
        render_project="ABCDEFG",
        render_owner="Whatever",
        study=study)
    rendered_volume = RenderedVolume(
        specimen=specimen,
        mipmap_directory="/Lorem/ipsum/dolor/sit/amet/consectetur")
    chuck = Chunk(
        size=20,
        object_state="Something",
        rendered_volume=rendered_volume)  # TODO: preceding and following
    assert str(chuck.rendered_volume.specimen.study) == study.name

@override_settings(
    CHUNK_DEFAULTS={
        'overlap': 2,
        'start_z': 1,
        'chunk_size': 5 })
def test_chunks_for_z_index():
    # TODO: 0?
    load_offset = 11
    cks_1 = Chunk.chunks_for_z_index(load_offset, 11)
    cks_2 = Chunk.chunks_for_z_index(load_offset, 12)
    cks_3 = Chunk.chunks_for_z_index(load_offset, 13)
    cks_4 = Chunk.chunks_for_z_index(load_offset, 14)
    cks_5 = Chunk.chunks_for_z_index(load_offset, 15)
    cks_6 = Chunk.chunks_for_z_index(load_offset, 16)
    cks_7 = Chunk.chunks_for_z_index(load_offset, 17)
    cks_8 = Chunk.chunks_for_z_index(load_offset, 18)
    cks_9 = Chunk.chunks_for_z_index(load_offset, 19)
    cks_10 = Chunk.chunks_for_z_index(load_offset, 20)
    cks_11 = Chunk.chunks_for_z_index(load_offset, 21)
    cks_12 = Chunk.chunks_for_z_index(load_offset, 22)

    assert [0] == cks_1
    assert [0] == cks_2
    assert [0] == cks_3
    assert [0, 1] == cks_4
    assert [0, 1] == cks_5
    assert [1] == cks_6 
    assert [1,2] == cks_7
    assert [1,2] == cks_8
    assert [2] == cks_9
    assert [2,3] == cks_10
    assert [2,3] == cks_11
    assert [3] == cks_12

@override_settings(
    CHUNK_DEFAULTS={ 'overlap': 2, 'start_z': 1, 'chunk_size': 5 })
def test_z_indices_for_chunk():
    cks_1 = Chunk.z_indices_for_chunk(0)
    assert [1,2,3,4,5] == cks_1


@pytest.fixture
def lots_of_montage_sets(section_factory,
                         cameras_etc):
    overlap = 5
    storage_directory = '/path/to/storage_directory'
    metafile = '/path/to/metafile'
    (camera, microscope, sample_holder) = cameras_etc

    montage_sets = []

    timezone.activate(pytz.timezone('US/Pacific'))

    for i in range(1,1000):
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

@pytest.mark.django_db
def test_chunk_queries(lots_of_montage_sets):
    for em_mset in lots_of_montage_sets:
        assert type(em_mset.get_section_z_index()) == int
        # chnk, _ = Chunk.associate_montage_set(em_mset)

@pytest.mark.django_db
@override_settings(
    CHUNK_DEFAULTS={
        'overlap': 8,
        'start_z': 1,
        'chunk_size': 50 })
def test_chunk_z_range(lots_of_montage_sets):
    montage_sets = lots_of_montage_sets

    chunk_set = set()
    
    for mset in montage_sets:
        chunk_set = chunk_set.union(
            set(Chunk.assign_montage_set_to_chunks(mset)))

    assert set(range(0, 24)) == set([c.computed_index for c in chunk_set])
