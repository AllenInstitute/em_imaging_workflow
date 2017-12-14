import pytest
from mock import Mock, patch
from development.strategies.create_tile_pairs_strategy \
    import CreateTilePairsStrategy

def test_get_input_data():
    em_mset = Mock()
    task = Mock()
    storage_directory = '/example/storage/directory'

    strategy = CreateTilePairsStrategy()

    with patch('os.path.exists', Mock(return_value=True)):
        with patch('os.makedirs'):
            inp = strategy.get_input(
                em_mset, storage_directory, task)

    assert inp is not None

