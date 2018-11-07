import pytest
from mock import Mock, patch
from workflow_engine.models.job import Job
from workflow_engine.models.task import Task
from workflow_engine.workflow_controller import WorkflowController
from development.models import EMMontageSet
from tests.strategies.at_em_fixtures import strategy_configurations
from development.strategies.two_d_python_solver_strategy \
    import TwoDPythonSolverStrategy
from django.test.utils import override_settings
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
import simplejson as json


@pytest.mark.django_db
def test_get_input_data(strategy_configurations):
    em_mset = Mock()
    em_mset.get_redo_parameters = Mock(return_value={})
    task = Mock()
    storage_directory = '/example/storage/directory'

    test_get_input_data.mock_inp = None

    data_mock = Mock()
    data_mock.data = Mock()

    def assign_mock_inp(x):
        test_get_input_data.mock_inp = x
        return data_mock

    dump_mock = Mock(return_value=data_mock)
    dump_mock.dump = Mock(
        return_value=data_mock,
        side_effect=assign_mock_inp)
    dump_mock.data = Mock()
    ema_schema = Mock(return_value=dump_mock)


    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            with patch('development.strategies.two_d_python_solver_strategy.EMA_Schema',
                       ema_schema,
                       create=True):
                strategy = TwoDPythonSolverStrategy()
                inp = strategy.get_input(
                    em_mset,
                    storage_directory,
                    task)

    ema_schema.assert_called_once()
    dump_mock.dump.assert_called_once()
    #dump_mock.dump.assert_called_once_with(None)
    assert test_get_input_data.mock_inp is not None

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
@pytest.mark.parametrize(
    'state', [
    EMMontageSet.STATE.EM_MONTAGE_SET_PROCESSING,
    EMMontageSet.STATE.EM_MONTAGE_SET_REDO_POINT_MATCH,
    EMMontageSet.STATE.EM_MONTAGE_SET_REDO_SOLVER,
])
def test_on_finishing(lots_of_montage_sets, state):
    em_mset = lots_of_montage_sets[0]
    results = Mock()
    job = Job(
        id=444,
        enqueued_object_id=em_mset.id)
    task = Task(id=333, job=job)
    strat = TwoDPythonSolverStrategy()
    strat.get_or_create_task_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')

    em_mset.object_state = state

    with patch.object(
        WorkflowController,
        'start_workflow'):
        strat.on_finishing(em_mset, results, task)
