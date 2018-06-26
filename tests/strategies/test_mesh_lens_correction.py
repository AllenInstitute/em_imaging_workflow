import pytest
from mock import patch, Mock
from development.models import ReferenceSet, state_machines
from workflow_engine.workflow_controller import WorkflowController
from tests.strategies.at_em_fixtures import strategy_configurations
from development.strategies.generate_mesh_lens_correction \
    import GenerateMeshLensCorrection
from .at_em_fixtures import mock_run_states
from django.test.utils import override_settings


@pytest.mark.django_db
@override_settings(
    FIJI_PATH='/path/to/fiji'
)
def test_get_input_data(strategy_configurations):
    enqueued_object = ReferenceSet(uid='deadbeef',
                                   manifest_path='manifest.json',
                                   project_path='/path/to/project')
    task = None
    storage_directory = '/example/storage/directory'

    strategy = GenerateMeshLensCorrection()
    inp = strategy.get_input(enqueued_object,
                             storage_directory,
                             task)

    assert inp['manifest_path'] == 'manifest.json'
    assert inp['fiji_path'] == '/path/to/fiji'
    assert inp is not None


@pytest.mark.django_db
def test_on_failure():
    ref_set = ReferenceSet(
        uid='deadbeef',
        manifest_path='manifest.json',
        project_path='/path/to/project',
        workflow_state=state_machines.states(ReferenceSet).PROCESSING)
    task = Mock()

    with patch.object(WorkflowController,
        'get_enqueued_object',
        Mock(return_value=ref_set)) as mock_get_enqueued:
        strategy = GenerateMeshLensCorrection()
        strategy.on_failure(task)

    assert ref_set.workflow_state == 'FAILED'
    mock_get_enqueued.assert_called_once()


@pytest.mark.django_db
def test_on_finishing(mock_run_states):
    ref_set = ReferenceSet(
        uid='deadbeef',
        manifest_path='manifest.json',
        project_path='/path/to/project',
        workflow_state=state_machines.states(ReferenceSet).PROCESSING)
    task = Mock()

    strategy = GenerateMeshLensCorrection()

    with patch.object(strategy, 'set_well_known_file') as swkf_mock:
        results = {'output_json': 'mock_out'}
        strategy.on_finishing(ref_set, results, task)

    assert ref_set.workflow_state == 'DONE'
    swkf_mock.assert_called_once_with(
        'mock_out',
        ref_set,
        'description',  # TODO: better name
        task)
