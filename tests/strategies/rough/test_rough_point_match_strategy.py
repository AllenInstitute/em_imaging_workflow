import pytest
from tests.strategies.at_em_fixtures import strategy_configurations
from mock import Mock, patch, mock_open
from workflow_engine.models.task import Task
from workflow_engine.models.job import Job
from django.test.utils import override_settings
from workflow_engine.workflow_controller import WorkflowController
from tests.fixtures.model_fixtures import (
    cameras_etc,
    section_factory,
    lots_of_montage_sets,
    lots_of_chunks
)
from at_em_imaging_workflow.strategies.rough.rough_point_match_strategy \
    import RoughPointMatchStrategy
from at_em_imaging_workflow.models.chunk_assignment import ChunkAssignment

@pytest.mark.django_db
@patch('at_em_imaging_workflow.strategies.rough.'
       'rough_point_match_strategy.RoughPointMatchStrategy.'
       'get_workflow_node_input_template',
       Mock(return_value={
            'SIFTsteps': 5,
            'render': { }
       } ))
def test_get_input_data(lots_of_chunks,
                        strategy_configurations):
    chnk_assign = ChunkAssignment.objects.first()

    task = Task(id=345)
    storage_directory = '/example/storage/directory'
    strategy = RoughPointMatchStrategy()
    strategy.create_log_configuration = Mock(
        return_value='/path/to/log/dir')
    strategy.get_or_create_task_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')

    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            with patch("builtins.open",
                       mock_open(read_data='{{ log_file_path }}')):
                inp = strategy.get_input(
                    chnk_assign,
                    storage_directory,
                    task)
    assert inp['SIFTsteps'] == 5

    assert inp['collection'] == 'chunk_rough_align_point_matches'
    assert inp['pairJson'] == '/rough/tile/pair/file'


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
def test_on_finishing(lots_of_chunks):
    chnk = lots_of_chunks[0]
    min_z = min(int(i) for i in chnk.get_z_mapping().keys())
    chnk_assign = lots_of_chunks[0].chunkassignment_set.get(
        section__z_index=min_z
    )

    results = { 'pairCount': 5 }
    job = Job(
        id=444,
        enqueued_object_id=chnk_assign.id)
    task = Task(id=333, job=job)
    strat = RoughPointMatchStrategy()
    strat.get_or_create_task_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')

    with patch.object(
        WorkflowController,
        'start_workflow'):
        strat.on_finishing(
            chnk_assign,
            results,
            task)

    cfg = chnk_assign.chunk.configurations.get(
        configuration_type='rough_tile_pair_file')

    assert (cfg.json_object[str(min_z)]["tile_pair_file"] ==
        '/rough/tile/pair/file')
    assert cfg.json_object[str(min_z)]["pairCount"] == 5
    # TODO: multinode spark doesn't write this file.
    #assert (cfg.json_object["1"]["point_match_output"] ==
    #    '/path/to/task/storage/directory/output_333.json')
