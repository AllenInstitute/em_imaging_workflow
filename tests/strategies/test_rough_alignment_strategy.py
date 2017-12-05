import pytest
from development.strategies.rough_alignment_strategy \
    import RoughAlignmentStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = RoughAlignmentStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

