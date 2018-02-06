from development.strategies.apply_rough_alignment_strategy \
    import ApplyRoughAlignmentStrategy
from django.test.utils import override_settings
from mock import Mock, patch


@override_settings(
    RENDER_SERVICE_URL='MOCK_URL',
    RENDER_SERVICE_PORT=9999,
    RENDER_SERVICE_USER='MOCK_USER',
    RENDER_CLIENT_SCRIPTS='/path/to/mock/client/scripts',
)
def test_get_input_data():
    chnk = Mock()
    chnk.get_render_project_name = Mock(
        return_value='MOCKSPECIMEN')
    chnk.z_range = Mock(
        return_value=(50,150))
    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = ApplyRoughAlignmentStrategy()
    inp = strategy.get_input(
        chnk,
        storage_directory,
        task)

    assert inp['render']['project'] == 'MOCKSPECIMEN'
    assert inp['render']['owner'] == 'MOCK_USER'
    assert inp['render']['port'] == 9999
    assert inp['render']['host'] == 'MOCK_URL'
    assert inp['render']['client_scripts'] == '/path/to/mock/client/scripts'

    assert inp['minZ'] == 50
    assert inp['maxZ'] == 150

    assert inp['montage_stack'] == 'em_2d_montage_solved'
    assert inp['prealigned_stack'] == 'em_2d_montage_lc'
    assert inp['lowres_stack'] == 'em_rough_align_solved_downsample_zs50_ze150'
    assert inp['output_stack'] == 'em_rough_align_zs50_ze150'

