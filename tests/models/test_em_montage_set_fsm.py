import pytest
from django_fsm import TransitionNotAllowed
from at_em_imaging_workflow.models import EMMontageSet


@pytest.fixture
def pending_em_mset():
    em_mset = EMMontageSet()

    return em_mset


@pytest.fixture
def processing_em_mset(pending_em_mset):
    em_mset = pending_em_mset
    em_mset.start_processing()

    return em_mset


@pytest.fixture
def qc_em_mset(processing_em_mset):
    em_mset = processing_em_mset
    em_mset.finish_processing()

    return em_mset


@pytest.fixture
def qc_redo_point_match_em_mset(qc_em_mset):
    em_mset = qc_em_mset
    em_mset.redo_point_match()

    return em_mset


@pytest.fixture
def qc_redo_solver_em_mset(qc_em_mset):
    em_mset = qc_em_mset
    em_mset.redo_point_match()

    return em_mset


@pytest.fixture
def qc_passed_em_mset(qc_em_mset):
    em_mset = qc_em_mset
    em_mset.pass_qc()

    return em_mset


@pytest.fixture
def qc_failed_em_mset(qc_em_mset):
    em_mset = qc_em_mset
    em_mset.fail_qc()

    return em_mset


def test_pending_default(pending_em_mset):
    assert pending_em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_PENDING


def test_start_processing(processing_em_mset):
    assert processing_em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_PROCESSING


def test_finish_processing(qc_em_mset):
    assert qc_em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_QC


def test_repeat_finish_processing(qc_em_mset):
    with pytest.raises(TransitionNotAllowed) as exc:
        qc_em_mset.finish_processing()

    assert 'finish_processing' in str(exc.value)


def test_qc_failed(qc_em_mset):
    em_mset = qc_em_mset
    em_mset.fail_qc()

    assert em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_QC_FAILED


def test_qc_passed(qc_em_mset):
    em_mset = qc_em_mset
    em_mset.pass_qc()

    assert em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_QC_PASSED


def test_redo_point_match(qc_failed_em_mset):
    em_mset = qc_failed_em_mset
    em_mset.redo_point_match()

    assert em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_REDO_POINT_MATCH


def test_redo_solver(qc_failed_em_mset):
    em_mset = qc_failed_em_mset
    em_mset.redo_solver()

    assert em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_REDO_SOLVER


def test_fail(qc_failed_em_mset):
    em_mset = qc_failed_em_mset
    em_mset.fail()

    assert em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_FAILED


def test_gap(qc_failed_em_mset):
    em_mset = qc_failed_em_mset
    em_mset.gap()

    assert em_mset.object_state == \
        EMMontageSet.STATE.EM_MONTAGE_SET_GAP

# def test_failed_from_processing(processing_em_mset):
#     em_mset = processing_em_mset
#     em_mset.fail()
# 
#     assert em_mset.object_state == \
#         EMMontageSet.STATE.LENS_CORRECTION_FAILED
# 
# 
# def test_failed_from_done(done_em_mset):
#     em_mset = done_em_mset
#     em_mset.fail()
# 
#     assert em_mset.object_state == \
#         EMMontageSet.STATE.LENS_CORRECTION_FAILED
# 
# def test_failed_from_failed(failed_em_mset):
#     em_mset = failed_em_mset
#     em_mset.fail()
# 
#     assert em_mset.object_state == \
#         EMMontageSet.STATE.LENS_CORRECTION_FAILED
# 
# def test_reset_pending_from_pending(pending_em_mset):
#     em_mset = pending_em_mset
#     em_mset.reset_pending()
# 
#     assert em_mset.object_state == \
#         EMMontageSet.STATE.LENS_CORRECTION_PENDING
# 
# def test_reset_pending_from_processing(processing_em_mset):
#     em_mset = processing_em_mset
#     em_mset.reset_pending()
# 
#     assert em_mset.object_state == \
#         EMMontageSet.STATE.LENS_CORRECTION_PENDING
# 
# def test_reset_pending_from_failed(failed_em_mset):
#     em_mset = failed_em_mset
#     em_mset.reset_pending()
# 
#     assert em_mset.object_state == \
#         EMMontageSet.STATE.LENS_CORRECTION_PENDING
