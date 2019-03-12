import pytest
from mock import Mock
from development.strategies.wait_for_manual_qc \
    import WaitForManualQc

reprocess_instructions = \
"""457488_8R\t7\tpoint_match\t0.5
457488_8R\t8\tpoint_match\t0.5
457488_8R\t9\tpoint_match\t0.5
"""


@pytest.mark.xfail
@pytest.mark.parametrize(
    'state,expected', [
    ('MONTAGE_QC_PASSED', False),
    ('MONTAGE_QC_FAILED', True),
    ('REIMAGE', True),
    ('PENDING', True),
    ('PROCESSING', True),
    ('MONTAGE_QC_FAILED_MOVE', False)])
def test_get_input_data(state,expected):
    em_mset = Mock()
    em_mset.object_state = state
    strategy = WaitForManualQc()

    assert strategy.must_wait(em_mset) == expected
