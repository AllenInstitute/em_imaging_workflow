from django.test import TestCase
from mock import patch
from development.models import ReferenceSet
from development.strategies.generate_lens_correction_transform_strategy \
    import GenerateLensCorrectionTransformStrategy
from development.strategies.schemas.generate_lens_correction_transform \
    import input_dict


class TestGenerateLensCorrectionTransformStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = ReferenceSet(uid='deadbeef',
                                       manifest_path='manifest.json',
                                       project_path='/path/to/project')
        task = None
        storage_directory = '/example/storage/directory'

        strategy = GenerateLensCorrectionTransformStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)

        assert input['manifest_path'] == 'manifest.json'
        assert input['fiji_path'] == input_dict['fiji_path']
        assert input is not None
