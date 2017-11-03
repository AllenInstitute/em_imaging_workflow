import django
django.setup()
from django.test import TestCase
from mock import Mock, patch
from development.strategies.create_tile_pairs_strategy \
    import CreateTilePairsStrategy

class TestCreateTilePairsStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = Mock()
        storage_directory = '/example/storage/directory'
        strategy = CreateTilePairsStrategy()
        with patch('os.makedirs'):
            input = strategy.get_input(enqueued_object,
                                       storage_directory,
                                       task)
        assert input is not None

