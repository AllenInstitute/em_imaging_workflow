from mock import Mock, patch, call
import pytest
from django.test.utils import override_settings
from workflow_engine.models.job import Job
from workflow_engine.models.task import Task
from development.strategies.move_raw_montage_set_strategy import MoveRawMontageSetStrategy
from development.strategies.move_reference_set_strategy \
    import MoveReferenceSetStrategy
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets


def test_get_input_data():
    enqueued_object = Mock()
    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = MoveReferenceSetStrategy()
    inp = strategy.get_input(enqueued_object,
                             storage_directory,
                             task)
    assert inp is not None


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
def test_on_finishing(lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    results = { 'tile_pair_file': '/path/to/tile/pair/file' }
    job = Job(
        id=444,
        enqueued_object_id=em_mset.id)
    task = Task(id=333, job=job)
    strat = MoveReferenceSetStrategy()
    em_mset.get_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')
    strat.set_well_known_file = Mock()

    with patch('os.system') as oss:
        strat.on_finishing(em_mset, results, task)

    assert oss.call_args_list == [
        call('find /path/to/task/storage/directory -type f -print -exec chmod go+r {} \\;'),
        call('find /path/to/task/storage/directory -type d -print -exec chmod go+rx {} \\;')
        ]

