import django
django.setup()
from django.test import TestCase
from development.strategies.fine_point_match_generation_strategy \
    import FinePointMatchGenerationStrategy

class TestFinePointMatchGenerationStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = FinePointMatchGenerationStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
        assert input is not None
