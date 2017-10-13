import django
django.setup()
from django.test import TestCase
from development.strategies.ingest_generate_render_stack_strategy \
    import IngestGenerateRenderStackStrategy

class TestIngestGenerateRenderStackStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = IngestGenerateRenderStackStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
        assert input is not None

