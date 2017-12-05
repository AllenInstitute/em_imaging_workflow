import pytest
from development.strategies.fine_alignment_q_c_strategy \
    import FineAlignmentQCStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = FineAlignmentQCStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None
