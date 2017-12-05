import pytest
from development.strategies.at_m_i_c_tasks_strategy \
    import ATMICTasksStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = ATMICTasksStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

