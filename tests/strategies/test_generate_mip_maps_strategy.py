import pytest
from django.test.utils import override_settings
from mock import Mock, patch
from workflow_engine.models.job import Job
from workflow_engine.models.task import Task
from workflow_engine.workflow_controller import WorkflowController
from at_em_imaging_workflow.strategies.montage.generate_mip_maps_strategy \
    import GenerateMipMapsStrategy
from tests.models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets


@pytest.mark.django_db
@patch(
    'at_em_imaging_workflow.strategies.montage.'
    'generate_mip_maps_strategy.GenerateMipMapsStrategy.'
    'get_workflow_node_input_template',
    Mock(return_value={})
)
@override_settings(
    RENDER_SERVICE_URL='MOCK_URL',
    RENDER_SERVICE_PORT=9999,
    RENDER_SERVICE_USER='MOCK_USER',
    RENDER_CLIENT_SCRIPTS='/path/to/mock/client/scripts',
    MIPMAP_FILE_PATH='/path/to/mipmaps',
)
def test_get_input_data(lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    task = Mock()
    task.job = Mock()
    storage_directory = '/example/storage/directory'
    strategy = GenerateMipMapsStrategy()
    
    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            inp = strategy.get_input(em_mset,
                                       storage_directory,
                                       task)
    assert inp['output_dir'].startswith('/path/to/mipmaps')
    assert set(inp['zValues']) == set([10000])


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
    results = { 'output_dir': '/path/to/output/dir' }
    job = Job(
        id=444,
        enqueued_object_id=em_mset.id)
    task = Task(id=333, job=job)
    strat = GenerateMipMapsStrategy()
    em_mset.get_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')
    strat.set_well_known_file = Mock()

    with patch.object(
        WorkflowController,
        'start_workflow'):
        strat.on_finishing(em_mset, results, task)
