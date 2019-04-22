import pytest
import django; django.setup()
from at_em_imaging_workflow.models import (
    Chunk,
    ChunkCalculator,
    RenderedVolume,
    Study,
    Specimen
)
from django.test.utils import override_settings
from tests.fixtures.model_fixtures import (
    cameras_etc,
    section_factory,
    lots_of_montage_sets
)


def xtest_str():
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

@pytest.mark.django_db
def xtest_chunk_queries(lots_of_montage_sets):
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

    volume_object = montage_sets[0].specimen().renderedvolume_set.first()

    chunk_set = set()

    load_object = montage_sets[0].get_load()

    computed_index = 999
    chunk_offset = 10000
    chunk_size = 1000
    chunk_overlap = 100 # TODO: use % 16

    chunk_0 = ChunkCalculator.create_chunk(
        load_object,
        997,
        10000,
        11100,
        volume_object
    )
    chunk_1 = ChunkCalculator.create_chunk(
        load_object,
        998,
        11000,
        12100,
        volume_object
    )
    chunk_2 = ChunkCalculator.create_chunk(
        load_object,
        999,
        12000,
        12999,
        volume_object
    )

    for mset in montage_sets:
        chunk_set = chunk_set.union(
            set(Chunk.assign_to_chunks(mset)))

    assert set([997]) == set([c.computed_index for c in chunk_set])
