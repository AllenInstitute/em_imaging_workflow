from mock import Mock
from development.strategies.m_i_c_tasks_strategy \
    import MICTasksStrategy


def test_get_input_data():
    enqueued_object = Mock()
    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = MICTasksStrategy()
    inp = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert inp is not None

