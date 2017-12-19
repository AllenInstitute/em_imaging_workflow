import pytest
from mock import Mock, patch
from development.strategies.two_d_montage_point_match_strategy \
    import TwoDMontagePointMatchStrategy

def test_get_input_data():
    em_mset = Mock()
    task = Mock()
    storage_directory = '/example/storage/directory'

    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            strategy = TwoDMontagePointMatchStrategy()
            inp = strategy.get_input(em_mset,
                                       storage_directory,
                                       task)
    assert inp is not None

