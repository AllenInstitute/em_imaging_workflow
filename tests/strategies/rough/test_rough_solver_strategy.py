import pytest
from mock import patch, Mock, mock_open
from workflow_engine.models.task import Task
from django.test.utils import override_settings
from development.strategies.rough.solve_rough_alignment_strategy \
    import SolveRoughAlignmentStrategy
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from strategies.rough.test_rough_point_match_strategy \
    import lots_of_chunks
import simplejson as json
try:
    import __builtin__ as builtins  # @UnresolvedImport
except:
    import builtins  # @UnresolvedImport


@pytest.mark.django_db
@override_settings(
    CHUNK_DEFAULTS={
        'overlap': 2,
        'start_z': 1,
        'chunk_size': 5 })
def test_get_input_data(lots_of_chunks):
    chnk = lots_of_chunks[2]
    task = Task(id=345)
    storage_directory = '/example/storage/directory'
    strategy = SolveRoughAlignmentStrategy()
    strategy.create_log_configuration = Mock(
        return_value='/path/to/log/dir')
    strategy.get_or_create_task_storage_directory = Mock(
        return_value='/path/to/task/storage/directory')

    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            with patch(builtins.__name__ + ".open",
                       mock_open(read_data='{{ log_file_path }}')):

                inp = strategy.get_input(
                    chnk,
                    storage_directory,
                    task)

    assert inp['first_section'] == 17
    assert inp['last_section'] == 26
    assert set(inp.keys()) == {
        'render',
        'log_level',
        'source_collection',
        'target_collection',
        'source_point_match_collection',
        'solver_executable',
        'first_section',
        'last_section',
        'solver_options',
        'verbose'}
    #assert json.dumps(inp, indent=2) == ''
