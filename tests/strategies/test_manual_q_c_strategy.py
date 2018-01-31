from mock import Mock
from development.strategies import RENDER_STACK_INGEST, RENDER_STACK_SOLVED
from development.strategies.manual_q_c_strategy \
    import ManualQCStrategy
from django.test.utils import override_settings
import simplejson as json


@override_settings(
    RENDER_SERVICE_URL='MOCK_URL',
    RENDER_SERVICE_PORT=9999,
    RENDER_SERVICE_USER='MOCK_USER',
    RENDER_CLIENT_SCRIPTS='/path/to/mock/client/scripts',
)
def test_get_input_data():
    em_mset = Mock()
    em_mset.get_point_collection_name = Mock(
        return_value='MOCK_COLLECTION')
    em_mset.get_render_project_name = Mock(
        return_value='MOCKSPECIMEN')
    em_mset.section = Mock()
    em_mset.section.specimen = Mock()
    em_mset.section.specimen.uid = \
        'MOCKSPECIMEN'
    em_mset.section.z_index = 1515
    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = ManualQCStrategy()

    inp = strategy.get_input(em_mset,
                             storage_directory,
                             task)

    with open('/local1/git/at_em_imaging_workflow/dbg.json', 'w') as f:
        f.write(json.dumps(inp, indent=4))

    assert inp['render']['project'] == 'MOCKSPECIMEN'
    assert inp['render']['owner'] == 'MOCK_USER'
    assert inp['render']['port'] == 9999
    assert inp['render']['host'] == 'MOCK_URL'
    assert inp['render']['client_scripts'] == '/path/to/mock/client/scripts'
    assert inp['prestitched_stack'] == RENDER_STACK_INGEST
    assert inp['poststitched_stack'] == RENDER_STACK_SOLVED
    assert inp['match_collection'] == 'MOCK_COLLECTION'
    assert inp['minZ'] == 1515
    assert inp['maxZ'] == 1515
