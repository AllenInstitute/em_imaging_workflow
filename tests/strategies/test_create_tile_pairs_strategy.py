import pytest
from mock import Mock, patch
from development.strategies.create_tile_pairs_strategy \
    import CreateTilePairsStrategy

def test_get_input_data():
    enqueued_object = None
    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = CreateTilePairsStrategy()
    with patch('os.makedirs'):
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
    assert input is not None

