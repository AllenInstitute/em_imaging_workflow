import django
django.setup()
from django.test import TestCase
from development.strategies.manual_q_c_strategy \
    import ManualQCStrategy

class TestManualQCStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = ManualQCStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
        assert input is not None

