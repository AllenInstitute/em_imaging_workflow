import pytest
from mock import Mock
from at_em_imaging_workflow.models import EMMontageSet
from at_em_imaging_workflow.strategies.montage.wait_for_manual_qc import (
    WaitForManualQc
)
from tests.models.test_chunk_model import (
    cameras_etc,          # noqa # pylint: disable=unused-import
    section_factory,      # noqa # pylint: disable=unused-import
    lots_of_montage_sets  # noqa # pylint: disable=unused-import
)


reprocess_instructions = \
"""457488_8R\t7\tpoint_match\t0.5
457488_8R\t8\tpoint_match\t0.5
457488_8R\t9\tpoint_match\t0.5
"""


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


@pytest.mark.parametrize(
    'state,expected', [
    ('MONTAGE_QC_PASSED', False),
    ('REIMAGE', False),
    ('MONTAGE_QC_FAILED', True),
    ('PENDING', True),
    ('PROCESSING', True)])
def test_must_wait(state,expected):
    em_mset = Mock()
    em_mset.object_state = state
    strategy = WaitForManualQc()

    assert strategy.must_wait(em_mset) == expected
