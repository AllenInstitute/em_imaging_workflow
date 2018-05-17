import pytest
from development.models.e_m_montage_set import EMMontageSet
from development.strategies.wait_for_manual_qc \
    import WaitForManualQc
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from development.models import state_machines


@pytest.mark.django_db
@pytest.mark.parametrize(
    'state,expected', [
    (state_machines.states(EMMontageSet).MONTAGE_QC_PASSED, False),
    (state_machines.states(EMMontageSet).MONTAGE_QC_FAILED, True),
    (state_machines.states(EMMontageSet).REIMAGE, True),
    (state_machines.states(EMMontageSet).PENDING, True),
    (state_machines.states(EMMontageSet).PROCESSING, True)])
def test_get_input_data(lots_of_montage_sets,
                        state,expected):
    em_mset = lots_of_montage_sets[0]
    em_mset.workflow_state = state
    strategy = WaitForManualQc()

    assert strategy.must_wait(em_mset) == expected
