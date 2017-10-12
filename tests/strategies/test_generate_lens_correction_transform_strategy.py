from django.test import TestCase
from mock import patch
from development.models import ReferenceSet
from development.strategies.generate_lens_correction_transform_strategy \
    import GenerateLensCorrectionTransformStrategy


class TestGenerateLensCorrectionTransformStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = ReferenceSet(uid='deadbeef',
                                       project_path='/path/to/project')
        task = None
        storage_directory = '/example/storage/directory'

        with patch('development.strategies.generate_lens_correction_transform_strategy.'
                   '.GenerateLensCorrectionTransformStrategy'
                   '.find_manifest_path',
                   return_value='manifest.json'):
            strategy = GenerateLensCorrectionTransformStrategy()
            input = strategy.get_input(enqueued_object,
                                       storage_directory,
                                       task)

        assert input['manifest_path'] == 'manifest.json'
        assert input['fiji_path'] == \
            GenerateLensCorrectionTransformStrategy.default_input['fiji_path']
        # print("input: " + str(input))
        assert input is not None
