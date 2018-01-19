from mock import Mock
import django
from django.conf import settings
django.setup()
from django.test import TestCase
from development.strategies.generate_render_stack_strategy \
    import GenerateRenderStackStrategy


class TestIngestGenerateRenderStackStrategy(TestCase):
    def test_get_input_data(self):
        em_set = Mock()
        em_set.section = Mock()
        test_z_index = 543
        em_set.section.z_index = test_z_index
        em_set.section.specimen.uid = 'mock_specimen_uid'
        em_set.metafile = '/path/to/test/meta.file'
        em_set.render_stack_name = Mock(return_value='test_stack')
        task = Mock()

        storage_directory = '/example/storage/directory'
        strategy = GenerateRenderStackStrategy()
        input_json = strategy.get_input(em_set,
                                        storage_directory,
                                        task)

        assert input_json['render']['host'] == settings.RENDER_SERVICE_URL
        assert input_json['render']['port'] == int(settings.RENDER_SERVICE_PORT)
        assert input_json['render']['owner'] == settings.RENDER_SERVICE_USER
        assert input_json['render']['project'] == em_set.section.specimen.uid
        assert input_json['stack'] == 'em_2d_montage_ingest'
        assert input_json['render']['client_scripts'] == \
            settings.RENDER_CLIENT_SCRIPTS
        assert input_json['metafile'] == em_set.metafile
        assert input_json['close_stack'] == False
        assert input_json['z_index'] == test_z_index

