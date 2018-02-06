from mock import Mock, patch
from development.strategies.apply_mip_maps_strategy \
    import ApplyMipMapsStrategy

def test_get_input_data():
    em_mset = Mock()
    task = Mock()
    task.job = Mock()
    storage_directory = '/example/storage/directory'
    strategy = ApplyMipMapsStrategy()
    
    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            inp = strategy.get_input(em_mset,
                                     storage_directory,
                                     task)

    assert inp['overwrite_zlayer'] == True

