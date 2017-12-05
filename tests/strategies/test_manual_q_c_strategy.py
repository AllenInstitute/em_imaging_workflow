import pytest
from development.strategies.manual_q_c_strategy \
    import ManualQCStrategy


def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = ManualQCStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

