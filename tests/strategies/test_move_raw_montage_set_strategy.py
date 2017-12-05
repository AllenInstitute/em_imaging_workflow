import pytest
from development.strategies.move_raw_montage_set_strategy \
    import MoveRawMontageSetStrategy


def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = MoveRawMontageSetStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None
