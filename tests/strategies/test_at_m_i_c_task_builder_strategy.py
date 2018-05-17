import pytest
from tests.strategies.at_em_fixtures import strategy_configurations
from development.strategies.at_m_i_c_task_builder_strategy \
    import ATMICTaskBuilderStrategy

@pytest.mark.django_db
def test_get_input_data(strategy_configurations):
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = ATMICTaskBuilderStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

