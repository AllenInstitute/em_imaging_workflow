import pytest
from development.strategies.two_d_montage_point_match_strategy \
    import TwoDMontagePointMatchStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = TwoDMontagePointMatchStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

