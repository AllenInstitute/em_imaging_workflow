from mock import Mock
from development.strategies.move_raw_montage_set_strategy \
    import MoveRawMontageSetStrategy


def test_get_input_data():
    enqueued_object = Mock()
    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = MoveRawMontageSetStrategy()
    inp = strategy.get_input(enqueued_object,
                             storage_directory,
                             task)
    assert inp is not None
