import pytest
from mock import Mock, patch
from workflow_engine.models.job import Job
from workflow_engine.models.task import Task
from workflow_engine.workflow_controller import WorkflowController
from tests.strategies.at_em_fixtures import strategy_configurations
from development.strategies.two_d_montage_solver_strategy \
    import TwoDMontageSolverStrategy
from django.test.utils import override_settings
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets


@pytest.mark.django_db
@patch('development.strategies.two_d_montage_solver_strategy'
       '.get_workflow_node_input_template',
       Mock(return_value={
           'render': {},
           'source_collection': {},
           'source_point_match_collection': {},
           'target_collection': { 'stack': '' },
           'solver_options': {} }))
def test_get_input_data(strategy_configurations):
    em_mset = Mock()
    em_mset.reimage_index = Mock(return_value=0)
    task = Mock()
    storage_directory = '/example/storage/directory'

    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            strategy = TwoDMontageSolverStrategy()
            inp = strategy.get_input(
                em_mset,
                storage_directory,
                task)

    assert inp['solver_options']['lambda_value'] == 1000
    assert inp['solver_options']['transfac'] == 1e-5


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
    results = Mock()
    job = Job(
        id=444,
        enqueued_object_id=em_mset.id)
    task = Task(id=333, job=job)
    strat = TwoDMontageSolverStrategy()
    strat.get_or_create_task_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')

    with patch.object(
        WorkflowController,
        'start_workflow'):
        strat.on_finishing(em_mset, results, task)
