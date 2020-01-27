import pytest
from mock import Mock, patch
import django
from django.conf import settings
django.setup()
from at_em_imaging_workflow.strategies.montage.generate_render_stack_strategy \
    import GenerateRenderStackStrategy


@pytest.mark.django_db
@patch(
    'at_em_imaging_workflow.strategies.montage.'
    'generate_render_stack_strategy.GenerateRenderStackStrategy.'
    'get_workflow_node_input_template',
    Mock(return_value={})
)
def test_get_input_data():
    em_set = Mock()
    em_set.get_render_project_name = Mock(
        return_value='MOCKSPECIMEN')

    em_set.section = Mock()
    test_z_index = 543
    em_set.section.z_index = test_z_index
    em_set.section.specimen.uid = 'mock_specimen_uid'
    em_set.metafile_uri = '/path/to/test/meta.file'
    em_set.reimage_index = Mock(return_value=0)
    em_set.render_stack_name = Mock(
        return_value='test_stack')
    task = Mock()

    storage_directory = '/example/storage/directory'
    strategy = GenerateRenderStackStrategy()
    input_json = strategy.get_input(em_set,
                                    storage_directory,
                                    task)

    assert (input_json['render']['host'] ==
        settings.RENDER_SERVICE_URL)
    assert (input_json['render']['port'] ==
        int(settings.RENDER_SERVICE_PORT))
    assert (input_json['render']['owner'] ==
        settings.RENDER_SERVICE_USER)
    assert (input_json['render']['project'] ==
        'MOCKSPECIMEN')
    assert (input_json['output_stack'] ==
        'em_2d_montage_ingest')
    assert (input_json['render']['client_scripts'] ==
        settings.RENDER_CLIENT_SCRIPTS)
    assert input_json['metafile_uri'] == em_set.metafile_uri
    assert input_json['close_stack'] == False
    assert set(input_json['zValues']) == set([test_z_index])

