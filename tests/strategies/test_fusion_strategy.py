import django
django.setup()
from django.test import TestCase
from development.strategies.fusion_strategy \
    import FusionStrategy

class TestFusionStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = FusionStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
        assert input is not None

