import django
django.setup()
from django.test import TestCase
from mock import patch
from development.models import ReferenceSet
from development.strategies import GenerateLensCorrectionTransformStrategy

class TestGenerateLensCorrectionTransformStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = ReferenceSet(uid='deadbeef',
                                       project_path='/path/to/project')
        task = None
        storage_directory = '/example/storage/directory'
        strategy = GenerateLensCorrectionTransformStrategy()

        with patch('development.strategies.GenerateLensCorrectionTransformStrategy.find_manifest_path',
                   return_value='manifest.json'):
            input = strategy.get_input(enqueued_object,
                                       storage_directory,
                                       task)

        assert input['manifest_path'] == 'manifest.json'
        assert input['fiji_path'] == GenerateLensCorrectionTransformStrategy.default_input['fiji_path']
        print("input: " + str(input))
        assert input is not None
