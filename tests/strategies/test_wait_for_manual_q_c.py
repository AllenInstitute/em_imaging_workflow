import pytest
from at_em_imaging_workflow.models import EMMontageSet
from at_em_imaging_workflow.strategies.montage.wait_for_manual_qc import (
    WaitForManualQc
)
from tests.models.test_chunk_model import (
    cameras_etc, section_factory, lots_of_montage_sets
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'state,expected', [
    (EMMontageSet.STATE.EM_MONTAGE_SET_QC_PASSED, False),
    (EMMontageSet.STATE.EM_MONTAGE_SET_QC_FAILED, True),
    (EMMontageSet.STATE.EM_MONTAGE_SET_REIMAGE, False),
    (EMMontageSet.STATE.EM_MONTAGE_SET_PENDING, True),
    (EMMontageSet.STATE.EM_MONTAGE_SET_PROCESSING, True)])
def test_get_input_data(lots_of_montage_sets,
                        state,expected):
    em_mset = lots_of_montage_sets[0]
    em_mset.object_state = state
    strategy = WaitForManualQc()

    assert strategy.must_wait(em_mset) == expected
