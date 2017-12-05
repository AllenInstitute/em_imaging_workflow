import pytest
from development.strategies.move_reference_set_strategy \
    import MoveReferenceSetStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = MoveReferenceSetStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

