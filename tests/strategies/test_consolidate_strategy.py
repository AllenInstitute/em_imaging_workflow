import pytest
from development.strategies.consolidate_strategy \
    import ConsolidateStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = ConsolidateStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None
