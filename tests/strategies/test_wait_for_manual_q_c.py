import pytest
from mock import Mock
from development.strategies.wait_for_manual_qc \
    import WaitForManualQc


@pytest.mark.parametrize(
    'state,expected', [
    ('MONTAGE_QC_PASSED', False),
    ('MONTAGE_QC_FAILED', True),
    ('REIMAGE', True),
    ('PENDING', True),
    ('PROCESSING', True)])
def test_get_input_data(state,expected):
    em_mset = Mock()
    em_mset.workflow_state = 'MONTAGE_QC_PASSED'
    strategy = WaitForManualQc()

    assert strategy.must_wait(em_mset) == True
