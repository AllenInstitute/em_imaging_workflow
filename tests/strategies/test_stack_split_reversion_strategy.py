import pytest
from development.strategies.stack_split_reversion_strategy \
    import StackSplitReversionStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = StackSplitReversionStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

