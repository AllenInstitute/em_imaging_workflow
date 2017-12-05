import pytest
from development.strategies.define_chunks_strategy \
    import DefineChunksStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = DefineChunksStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

