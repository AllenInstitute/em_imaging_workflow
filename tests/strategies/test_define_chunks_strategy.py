from mock import Mock, patch
import pytest
from django.test.utils import override_settings
from workflow_engine.models.job import Job
from workflow_engine.models.task import Task
from development.models.e_m_montage_set import EMMontageSet
from development.strategies.chmod_strategy \
    import ChmodStrategy
from development.strategies.define_chunks_strategy \
    import DefineChunksStrategy
from development.models.chunk import Chunk
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets


@pytest.mark.django_db
@override_settings(
    DRY_RUN=False,
    BASE_FILE_PATH='/base',
    LONG_TERM_BASE_FILE_PATH='/long/term',
    RENDER_STACK_NAME='test_stack',
    RENDER_SERVICE_USER='test_user',
    RENDER_SERVICE_URL='test_render_host',
    RENDER_SERVICE_PORT='1234',
    RENDER_CLIENT_SCRIPTS='/path/to/test/client/scripts'
    )
def test_must_wait(lots_of_montage_sets):
    assert Chunk.objects.count() == 0

    for em_mset in lots_of_montage_sets:
        strat = DefineChunksStrategy()
        strat.must_wait(em_mset)

    pending = [
        ChmodStrategy.CHMOD_DIR_PENDING,
        ChmodStrategy.CHMOD_FILE_PENDING]

    assert Chunk.objects.count() == 125
    assert EMMontageSet.objects.count() == 999

    wkfs = ChmodStrategy.find_chmod_files(
        em_mset,
        type_list=pending)

    for w in wkfs:
        assert w.well_known_file_type in pending
