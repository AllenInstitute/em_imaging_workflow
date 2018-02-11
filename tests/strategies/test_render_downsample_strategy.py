import django; django.setup()
from django.test.utils import override_settings
from mock import Mock, patch, mock_open
from development.strategies.render_downsample_strategy \
    import RenderDownsampleStrategy

try:
    import __builtin__ as builtins  # @UnresolvedImport
except:
    import builtins  # @UnresolvedImport

@override_settings(
    BASE_FILE_PATH='/base',
    RENDER_STACK_NAME='test_stack',
    RENDER_SERVICE_USER='test_user',
    RENDER_SERVICE_URL='test_render_host',
    RENDER_SERVICE_PORT='1234',
    RENDER_CLIENT_SCRIPTS='/path/to/test/client/scripts'
    )
def test_get_input_data():
    em_mset = Mock()
    em_mset.get_render_project_name = Mock(
        return_value='test_project')
    em_mset.section.z_index = 92384
    em_mset.id = 9876
    task = Mock()
    task.id = 333
    task.job = Mock()
    task.job.id = 444
    task.job.get_enqueued_object = Mock(return_value=em_mset)     
    storage_directory = '/example/storage/directory'
    strategy = RenderDownsampleStrategy()
    
    file_str = '{ "transform": "MOCK_TRANSFORM" }'

    with patch('workflow_engine.models.well_known_file.WellKnownFile.get',
               Mock(return_value='/path/to/wkf')):
        with patch('os.makedirs'):
            with patch('subprocess.call'):
                with patch(builtins.__name__ + ".open",
                           mock_open(read_data=file_str)):
                    inp = strategy.get_input(
                        em_mset,
                        storage_directory,
                        task)

    assert inp['input_stack'] == 'em_2d_montage_solved'
    assert inp['render']['owner'] == 'test_user'
    assert inp['render']['host'] == 'test_render_host'
    assert inp['render']['port'] == 1234
    assert inp['render']['project'] == 'test_project'
    assert inp['render']['client_scripts'] == '/path/to/test/client/scripts'
    assert inp['minZ'] == 92384
    assert inp['maxZ'] == 92384
    assert inp['image_directory'] == '/base/9876/jobs/job_444/tasks/task_333'

    # useful for debugging
    # import simplejson as json; assert json.dumps(inp, indent=2) == ''
    
