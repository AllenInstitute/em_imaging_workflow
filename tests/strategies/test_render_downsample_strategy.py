from django.test.utils import override_settings
from mock import Mock, patch, mock_open
from workflow_engine.models.job import Job
from workflow_engine.models.task import Task
import pytest
from workflow_engine.workflow_controller import WorkflowController
from tests.strategies.at_em_fixtures import strategy_configurations
from development.strategies.render_downsample_strategy \
    import RenderDownsampleStrategy
from tests.models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets


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
def test_get_input_data(lots_of_montage_sets,
                        strategy_configurations):
    em_mset = lots_of_montage_sets[0]
    job = Job(
        id=444,
        enqueued_object_id=em_mset.id)
    task = Task(id=333, job=job)
    storage_directory = '/example/storage/directory'
    strategy = RenderDownsampleStrategy()
    
    file_str = '{ "transform": "MOCK_TRANSFORM" }'

    with patch('workflow_engine.models.well_known_file.WellKnownFile.get',
               Mock(return_value='/path/to/wkf')):
        with patch('os.makedirs'):
            with patch('subprocess.call'):
                with patch('builtins.open',
                           mock_open(read_data=file_str)):
                    inp = strategy.get_input(
                        em_mset,
                        storage_directory,
                        task)

    assert inp['input_stack'] == 'em_2d_montage_solved'
    assert inp['render']['owner'] == 'test_user'
    assert inp['render']['host'] == 'test_render_host'
    assert inp['render']['port'] == 1234
    assert inp['render']['project'] == 'MOCK SPECIMEN'
    assert inp['render']['client_scripts'] == '/path/to/test/client/scripts'
    assert inp['minZ'] == 1
    assert inp['maxZ'] == 1
    assert inp['image_directory'].startswith('/long/term')

    # useful for debugging
    # import simplejson as json; assert json.dumps(inp, indent=2) == ''


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
    results = { 'temp_stack': 'mock_stack'}
    job = Job(
        id=444,
        enqueued_object_id=em_mset.id)
    task = Task(id=333, job=job)
    strat = RenderDownsampleStrategy()

    with patch.object(
        WorkflowController,
        'start_workflow'):
        strat.on_finishing(em_mset, results, task)
