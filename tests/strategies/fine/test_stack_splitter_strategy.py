import pytest
from at_em_imaging_workflow.strategies.fine.stack_splitter_strategy \
    import StackSplitterStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = StackSplitterStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None

