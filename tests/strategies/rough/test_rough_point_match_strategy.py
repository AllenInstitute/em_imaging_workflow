import os
from tests.strategies.at_em_fixtures import strategy_configurations
os.environ['BLUE_SKY_SETTINGS'] = '/local1/git/at_em_imaging_workflow/at_em_imaging_workflow/blue_sky_settings.yml'

import pytest
from mock import Mock, patch, mock_open
from workflow_engine.models.task import Task
from workflow_engine.models.job import Job
from django.test.utils import override_settings
from workflow_engine.workflow_controller import WorkflowController
from development.models.chunk import Chunk
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from development.strategies.rough.rough_point_match_strategy \
    import RoughPointMatchStrategy
from development.models.chunk_assignment import ChunkAssignment

@pytest.fixture
def lots_of_chunks(lots_of_montage_sets):
    chnks = set()

    for em_mset in lots_of_montage_sets:
        chnks.update(
            Chunk.assign_montage_set_to_chunks(em_mset))

    return list(chnks)


@pytest.mark.django_db
@patch('development.strategies.rough'
       '.rough_point_match_strategy'
       '.get_workflow_node_input_template',
       Mock(return_value={
            'SIFTsteps': 5,
            'render': { }
       } ))
def test_get_input_data(lots_of_chunks,
                        strategy_configurations):
    chnk_assign = ChunkAssignment.objects.first()
    tpj = { "1": { "tile_pair_file": "/path/to/file" }}
    chnk_assign.chunk.configurations.update_or_create(
        configuration_type='rough_tile_pair_file',
        json_object=tpj)
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
    assert inp['pairJson'] == '/path/to/file'


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
    chnk_assign = ChunkAssignment.objects.first()
    tpj = { "1": { "tile_pair_file": "/path/to/file" }}
    cfg, _ = chnk_assign.chunk.configurations.update_or_create(
        configuration_type='rough_tile_pair_file',
        json_object=tpj)
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

    assert cfg.json_object["1"]["tile_pair_file"] == \
        '/path/to/file'
    assert cfg.json_object["1"]["pairCount"] == 5
    assert cfg.json_object["1"]["point_match_output"] == \
        '/path/to/task/storage/directory/output_333.json'
