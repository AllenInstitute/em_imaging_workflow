import pytest
from development.strategies.point_match_generation_strategy \
    import PointMatchGenerationStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = PointMatchGenerationStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

