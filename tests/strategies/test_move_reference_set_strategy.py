from mock import Mock
from development.strategies.move_reference_set_strategy \
    import MoveReferenceSetStrategy

def test_get_input_data():
    enqueued_object = Mock()
    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = MoveReferenceSetStrategy()
    inp = strategy.get_input(enqueued_object,
                             storage_directory,
                             task)
    assert inp is not None

