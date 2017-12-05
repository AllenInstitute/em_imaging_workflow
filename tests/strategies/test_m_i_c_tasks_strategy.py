import pytest
from development.strategies.m_i_c_tasks_strategy \
    import MICTasksStrategy


def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = MICTasksStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

