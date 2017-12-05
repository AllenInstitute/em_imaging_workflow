import pytest
from development.strategies.fine_point_match_generation_strategy \
    import FinePointMatchGenerationStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = FinePointMatchGenerationStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None
