import pytest
from mock import patch, Mock
from development.models import ReferenceSet
from workflow_engine.workflow_controller import WorkflowController
from workflow_engine.models.configuration import Configuration
from tests.strategies.at_em_fixtures import strategy_configurations
from development.strategies.generate_lens_correction_transform_strategy \
    import GenerateLensCorrectionTransformStrategy
from .at_em_fixtures import mock_run_states
from django.test.utils import override_settings


@pytest.mark.django_db
@pytest.mark.skipif(True,reason='needs better mocking')
@override_settings(
    FIJI_PATH='/path/to/fiji'
)
def test_get_input_data(strategy_configurations):
    enqueued_object = ReferenceSet(uid='deadbeef',
                                   manifest_path='manifest.json',
                                   project_path='/path/to/project')
    task = Mock()
    task.job = Mock()
    task.job.workflow_node = Mock()

    cfg = Configuration(
        content_object=task.job.workflow_node,
        name='Generate Mesh Lens Correction Input',
        configuration_type='strategy_config',
        json_object={})

    storage_directory = '/example/storage/directory'

    strategy = GenerateLensCorrectionTransformStrategy()
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
        object_state=ReferenceSet.STATE.LENS_CORRECTION_PROCESSING)
    task = Mock()

    with patch.object(WorkflowController,
        'get_enqueued_object',
        Mock(return_value=ref_set)) as mock_get_enqueued:
        strategy = GenerateLensCorrectionTransformStrategy()
        strategy.on_failure(task)

    assert ref_set.object_state == 'FAILED'
    mock_get_enqueued.assert_called_once()


@pytest.mark.django_db
def test_on_finishing(mock_run_states):
    ref_set = ReferenceSet(
        uid='deadbeef',
        manifest_path='manifest.json',
        project_path='/path/to/project',
        object_state=ReferenceSet.STATE.LENS_CORRECTION_PROCESSING)
    task = Mock()

    strategy = GenerateLensCorrectionTransformStrategy()

    with patch.object(strategy, 'set_well_known_file') as swkf_mock:
        results = {'output_json': 'mock_out'}
        strategy.on_finishing(ref_set, results, task)

    assert ref_set.object_state == 'DONE'
    swkf_mock.assert_called_once_with(
        'mock_out',
        ref_set,
        'description',  # TODO: better name
        task)
