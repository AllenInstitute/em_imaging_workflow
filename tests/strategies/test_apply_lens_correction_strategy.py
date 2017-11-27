import django
django.setup()
from django.test import TestCase
from development.strategies.apply_lens_correction_strategy \
    import ApplyLensCorrectionStrategy
from mock import patch, mock_open, MagicMock
try:
    import __builtin__ as builtins  # @UnresolvedImport
except:
    import builtins  # @UnresolvedImport

class TestApplyLensCorrectionStrategy(TestCase):
    def test_get_input_data(self):
        em_mset = MagicMock()
        em_mset.section = MagicMock()
        test_z_index = 543
        em_mset.section.z_index = test_z_index
        em_mset.metafile = '/path/to/test/meta.file'
        task = MagicMock()
        wkf_mock = MagicMock()
        wkf_mock.get = MagicMock(return_value='/path/to/xform.json')
        storage_directory = '/example/storage/directory'
        strategy = ApplyLensCorrectionStrategy()
        with patch('workflow_engine.models.well_known_file.WellKnownFile',
                   wkf_mock):
            with patch(builtins.__name__ + ".open",
                       mock_open(read_data='{ "transform": "TEST_XFM" }')):
                input_ret = strategy.get_input(em_mset,
                                               storage_directory,
                                               task)

        print(str(input_ret))
        assert input_ret is not None

