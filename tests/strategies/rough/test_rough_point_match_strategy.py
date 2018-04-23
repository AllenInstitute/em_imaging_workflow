import os
os.environ['BLUE_SKY_SETTINGS'] = '/local1/git/at_em_imaging_workflow/at_em_imaging_workflow/blue_sky_settings.yml'

import pytest
from mock import Mock, patch, mock_open
from workflow_engine.models.task import Task
from workflow_engine.models.job import Job
from django.test.utils import override_settings
from workflow_engine.workflow_controller import WorkflowController
from development.strategies.chmod_strategy import ChmodStrategy
from development.models.chunk import Chunk
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from development.strategies.rough.rough_point_match_strategy \
    import RoughPointMatchStrategy

@pytest.fixture
def lots_of_chunks(lots_of_montage_sets):
    chnks = set()

    for em_mset in lots_of_montage_sets:
        chnks.update(
            Chunk.assign_montage_set_to_chunks(em_mset))

    return list(chnks)


@pytest.mark.django_db
def test_get_input_data(lots_of_chunks):
    chnk = lots_of_chunks[0]
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
                    chnk,
                    storage_directory,
                    task)
    assert inp['clipWidth'] == 800
    assert inp['clipHeight'] == 800
    assert inp['SIFTsteps'] == 3
    assert inp['memory'] == '4g'
    assert inp['SIFTfdSize'] == 8
    assert inp['SIFTmaxScale'] == 0.82
    assert inp['SIFTminScale'] == 0.38
    assert inp['renderScale'] == 0.4

    assert inp['collection'] == 'chunk_point_matches'
    assert inp['pairJson'] == None


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
    results = { 'pairCount': 5 }
    job = Job(
        id=444,
        enqueued_object_id=em_mset.id)
    task = Task(id=333, job=job)
    strat = RoughPointMatchStrategy()
    strat.get_or_create_task_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')

    with patch('os.path.exists',
               Mock(return_value=True)) as ope:
        with patch.object(
            WorkflowController,
            'start_workflow'):
            strat.on_finishing(em_mset, results, task)

    ope.assert_called_once_with(
        '/path/to/task/storage/directory/output_333.json')
    pending = [
        ChmodStrategy.CHMOD_DIR_PENDING,
        ChmodStrategy.CHMOD_FILE_PENDING]

    wkfs = ChmodStrategy.find_chmod_files(
        em_mset,
        type_list=pending)

    assert len(wkfs) == 0
