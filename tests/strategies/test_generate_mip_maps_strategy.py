import pytest
from development.strategies.generate_mip_maps_strategy \
    import GenerateMipMapsStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = GenerateMipMapsStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

