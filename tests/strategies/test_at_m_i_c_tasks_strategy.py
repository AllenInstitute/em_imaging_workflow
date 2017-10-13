import django
django.setup()
from django.test import TestCase
from development.strategies.at_m_i_c_tasks_strategy \
    import ATMICTasksStrategy

class TestATMICTasksStrategy(TestCase):
    def test_get_input_data(self):
        enqueued_object = None
        task = None
        storage_directory = '/example/storage/directory'
        strategy = ATMICTasksStrategy()
        input = strategy.get_input(enqueued_object,
                                   storage_directory,
                                   task)
        assert input is not None

