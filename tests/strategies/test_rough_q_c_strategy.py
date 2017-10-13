import django
django.setup()
from django.test import TestCase
from development.strategies.rough_q_c_strategy \
    import RoughQCStrategy

class TestRoughQCStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = RoughQCStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
        assert input is not None

