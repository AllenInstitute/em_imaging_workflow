import django
django.setup()
from django.test import TestCase
from development.strategies.fine_alignment_q_c_strategy \
    import FineAlignmentQCStrategy

class TestFineAlignmentQCStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = FineAlignmentQCStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
        assert input is not None
