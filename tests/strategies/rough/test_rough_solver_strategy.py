import pytest
from mock import patch, Mock, mock_open
from workflow_engine.models.task import Task
from django.test.utils import override_settings
from tests.strategies.at_em_fixtures import strategy_configurations
from development.strategies.rough.solve_rough_alignment_strategy \
    import SolveRoughAlignmentStrategy
from tests.models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from tests.strategies.rough.test_rough_point_match_strategy \
    import lots_of_chunks


@pytest.mark.django_db
@override_settings(
    RENDER_SERVICE_URL='MOCK_URL',
    RENDER_SERVICE_PORT=9999,
    RENDER_SERVICE_USER='MOCK_USER',
    RENDER_CLIENT_SCRIPTS='/path/to/mock/client/scripts',
    CHUNK_DEFAULTS={
        'overlap': 2,
        'start_z': 1,
        'chunk_size': 5 })
@patch('development.strategies.rough'
       '.solve_rough_alignment_strategy'
       '.get_workflow_node_input_template',
       Mock(return_value={
           'montage_stack': "",
           'source_collection': { 'stack': '' },
           'solver_options': {},
           'source_point_match_collection': {
               'match_collection': '' 
            },
           'target_collection': { 'stack': '' },
           'output_stack': "",
           'render': { 'source_collection': '' } } ))
def test_get_input_data(lots_of_chunks,
                        strategy_configurations):
    chnk = lots_of_chunks[2]
    chnk.configurations.update_or_create(
        name='chunk 2 configuration',
        configuration_type='chunk_configuration',
        defaults={
            'json_object': { 'tile_pair_ranges': {
                "1": { "minz": 2,
                      "maxz": 2
                    }
                } } })
    task = Task(id=345)
    storage_directory = '/example/storage/directory'
    strategy = SolveRoughAlignmentStrategy()
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

    assert inp['first_section'] == 2
    assert inp['last_section'] == 2
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
