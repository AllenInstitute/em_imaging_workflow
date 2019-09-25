from mock import Mock, patch
import pytest
from django.test.utils import override_settings
from workflow_engine.models import Job, Task
from workflow_engine.workflow_controller import WorkflowController
from at_em_imaging_workflow.strategies.montage.apply_mip_maps_strategy \
    import ApplyMipMapsStrategy
from tests.models.test_chunk_model import (
    cameras_etc,          # noqa # pylint: disable=unused-import
    section_factory,      # noqa # pylint: disable=unused-import
    lots_of_montage_sets  # noqa # pylint: disable=unused-import
)
from tests.strategies.at_em_fixtures import (
    strategy_configurations  # noqa # pylint: disable=unused-import
)


@pytest.mark.django_db
def test_get_input_data(lots_of_montage_sets,
                        strategy_configurations):
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
    assert set(inp['zValues']) == set([10000])
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
                      'start_workflow'):
        strat.on_finishing(em_mset, results, task)
