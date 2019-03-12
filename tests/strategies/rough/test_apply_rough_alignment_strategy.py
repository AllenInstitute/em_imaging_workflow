from workflow_engine.models.task import Task
import pytest
from tests.strategies.at_em_fixtures import strategy_configurations
from development.strategies.rough.apply_rough_alignment_strategy \
    import ApplyRoughAlignmentStrategy
from tests.models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from tests.strategies.rough.test_rough_point_match_strategy \
    import lots_of_chunks
from django.test.utils import override_settings
from mock import Mock, patch


@pytest.mark.skipif(True, reason='unimplemented')
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
def test_get_input_data(lots_of_chunks,
                        strategy_configurations):
    chnk = lots_of_chunks[2]
    task = Task(id=345)
#     chnk.get_render_project_name = Mock(
#         return_value='MOCKSPECIMEN')
#     chnk.z_range = Mock(
#         return_value=(50,150))
#     task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = ApplyRoughAlignmentStrategy()
    inp = strategy.get_input(
        chnk,
        storage_directory,
        task)

    assert inp['render']['project'] == 'MOCK SPECIMEN'
    assert inp['render']['owner'] == 'MOCK_USER'
    assert inp['render']['port'] == 9999
    assert inp['render']['host'] == 'MOCK_URL'
    assert inp['render']['client_scripts'] == '/path/to/mock/client/scripts'

    assert inp['minZ'] == 17
    assert inp['maxZ'] == 26

    assert inp['montage_stack'] == 'em_2d_montage_solved'
    assert inp['prealigned_stack'] == 'em_2d_montage_lc'
    assert inp['lowres_stack'] == 'em_rough_align_solved_downsample_zs17_ze26'
    assert inp['output_stack'] == 'em_rough_align_zs17_ze26'

