import pytest
from at_em_imaging_workflow.strategies.fine.fine_q_c_strategy \
    import FineQCStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = FineQCStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None
