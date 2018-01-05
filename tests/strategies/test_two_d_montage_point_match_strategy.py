import pytest
from mock import Mock, patch, mock_open
from development.strategies.two_d_montage_point_match_strategy \
    import TwoDMontagePointMatchStrategy
try:
    import __builtin__ as builtins  # @UnresolvedImport
except:
    import builtins  # @UnresolvedImport


@pytest.mark.xfail
def test_get_input_data():
    em_mset = Mock()
    task = Mock()
    storage_directory = '/example/storage/directory'

    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            with patch(builtins.__name__ + ".open",
                       mock_open(read_data='{{ log_file_path }}')):
                strategy = TwoDMontagePointMatchStrategy()
                inp = strategy.get_input(em_mset,
                                           storage_directory,
                                           task)
    assert inp is not None

