import pytest
from mock import patch, Mock, mock_open
from workflow_engine.models.task import Task
from django.test.utils import override_settings
from at_em_imaging_workflow.strategies.rough.solve_rough_alignment_python \
    import SolveRoughAlignmentPython
from tests.fixtures.model_fixtures import (
    cameras_etc,           # noqa # pylint: disable=unused-import
    section_factory,       # noqa # pylint: disable=unused-import
    lots_of_montage_sets,  # noqa # pylint: disable=unused-import
    lots_of_chunks         # noqa # pylint: disable=unused-import
)


@pytest.mark.render_schema_failure
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
@patch.object(
    SolveRoughAlignmentPython,
    'get_workflow_node_input_template',
    Mock(return_value={
      "pointmatch": {
        "name": "",
        "port": 0,
        "owner": "",
        "mongo_host": "",
        "mongo_port": 0,
        "db_interface": "",
        "client_scripts": "",
        "collection_type": "pointmatch"
      },
      "solve_type": "3D",
      "close_stack": False,
      "input_stack": {
        "host": "",
        "name": "",
        "port": 0,
        "owner": "",
        "project": "",
        "mongo_host": "",
        "mongo_port": 0,
        "db_interface": "",
        "client_scripts": "",
        "collection_type": "stack"
      },
      "output_mode": "stack",
      "hdf5_options": {
        "output_dir": "",
        "chunks_per_file": 1
      },
      "last_section": 0,
      "output_stack": {
        "host": "",
        "name": "",
        "port": 0,
        "owner": "",
        "project": "",
        "mongo_host": "",
        "mongo_port": 0,
        "db_interface": "",
        "client_scripts": "",
        "collection_type": "stack"
      },
      "first_section": 0,
      "regularization": {
        "default_lambda": 10000000.0,
        "translation_factor": 1e-10
      },
      "transformation": "rigid",
      "matrix_assembly": {
        "depth": 3,
        "npts_max": 500,
        "npts_min": 5,
        "inverse_dz": "True",
        "cross_pt_weight": 0.5,
        "montage_pt_weight": 1.0
      },
      "n_parallel_jobs": 32,
      "start_from_file": ""
    })
)
def test_get_input_data(lots_of_chunks):
    chnk = lots_of_chunks[2]

    task = Task(id=345)
    storage_directory = '/example/storage/directory'
    strategy = SolveRoughAlignmentPython()
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

    assert inp['first_section'] == 180
    assert inp['last_section'] == 280

    assert set(inp.keys()) == {
        'render_output',
        'output_mode',
        'close_stack',
        'last_section',
        'first_section',
        'regularization',
        'ingest_from_file',
        'assemble_from_file',
        'showtiming',
        'n_parallel_jobs',
        'output_stack',
        'profile_data_load',
        'transformation',
        'pointmatch',
        'log_level',
        'overwrite_zlayer',
        'hdf5_options',
        'solve_type',
        'input_stack',
        'matrix_assembly'
    }
