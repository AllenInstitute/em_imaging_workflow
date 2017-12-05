import pytest
from development.strategies.two_d_montage_solver_strategy \
    import TwoDMontageSolverStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = TwoDMontageSolverStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

