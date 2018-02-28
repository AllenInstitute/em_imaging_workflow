from mock import Mock, patch
import pytest
from django.test.utils import override_settings
from workflow_engine.models.job import Job
from workflow_engine.models.task import Task
from workflow_engine.workflow_controller import WorkflowController
from development.strategies.chmod_strategy import ChmodStrategy
from development.strategies.apply_mip_maps_strategy \
    import ApplyMipMapsStrategy
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
import simplejson as json


@pytest.mark.django_db
def test_get_input_data(lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    task = Mock()
    task.job = Mock()
    storage_directory = '/example/storage/directory'
    strategy = ApplyMipMapsStrategy()
    
    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            inp = strategy.get_input(em_mset,
                                     storage_directory,
                                     task)

    assert inp['overwrite_zlayer'] == True
    assert set(inp['zValues']) == set([1])
    assert inp['input_stack'] == 'em_2d_montage_ingest'
    assert inp['output_stack'] == 'em_2d_montage_apply_mipmaps'
    assert inp['pool_size'] == 20

@pytest.mark.django_db
@override_settings(
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
    strat = ApplyMipMapsStrategy()
    em_mset.get_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')
    em_mset.mipmap_directory='/path/to/mipmap/directory'
    strat.set_well_known_file = Mock()

    with patch.object(WorkflowController,
                      'start_workflow') as strt:
        strat.on_finishing(em_mset, results, task)

    pending = [
        ChmodStrategy.CHMOD_DIR_PENDING,
        ChmodStrategy.CHMOD_FILE_PENDING]

    wkfs = ChmodStrategy.find_chmod_files(
        em_mset,
        type_list=pending)

    assert len(wkfs) == 4

    for w in wkfs:
        assert w.well_known_file_type in pending

    strt.assert_called_once_with(
        'em_2d_montage',
        em_mset,
        start_node_name='Chmod Montage')
