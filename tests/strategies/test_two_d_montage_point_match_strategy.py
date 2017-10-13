import django
django.setup()
from django.test import TestCase
from development.strategies.two_d_montage_point_match_strategy \
    import TwoDMontagePointMatchStrategy

class TestTwoDMontagePointMatchStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = TwoDMontagePointMatchStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
        assert input is not None

