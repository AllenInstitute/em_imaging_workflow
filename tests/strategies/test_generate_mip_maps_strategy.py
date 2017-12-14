import pytest
from mock import Mock, patch
from development.strategies.generate_mip_maps_strategy \
    import GenerateMipMapsStrategy

def test_get_input_data():
    em_mset = Mock()
    task = Mock()
    task.job = Mock()
    storage_directory = '/example/storage/directory'
    strategy = GenerateMipMapsStrategy()
    
    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            input = strategy.get_input(em_mset,
                                       storage_directory,
                                       task)
            assert input is not None

