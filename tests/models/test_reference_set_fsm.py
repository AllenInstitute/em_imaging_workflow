import pytest
from django_fsm import TransitionNotAllowed
from development.models import ReferenceSet


@pytest.fixture
def pending_ref_set():
    ref_set = ReferenceSet()

    return ref_set


@pytest.fixture
def processing_ref_set(pending_ref_set):
    ref_set = pending_ref_set
    ref_set.start_processing()

    return ref_set


@pytest.fixture
def done_ref_set(processing_ref_set):
    ref_set = processing_ref_set
    ref_set.finish_processing()

    return ref_set


@pytest.fixture
def failed_ref_set(processing_ref_set):
    ref_set = processing_ref_set
    ref_set.fail()

    return ref_set


def test_pending_default(pending_ref_set):
    assert pending_ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_PENDING


def test_start_processing(processing_ref_set):
    assert processing_ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_PROCESSING


def test_finish_processing(done_ref_set):
    assert done_ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_DONE


def test_repeat_done(done_ref_set):
    with pytest.raises(TransitionNotAllowed) as exc:
        done_ref_set.finish_processing()

    assert 'DONE' in str(exc.value)


def test_failed_from_pending(pending_ref_set):
    ref_set = pending_ref_set
    ref_set.fail()

    assert ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_FAILED


def test_failed_from_processing(processing_ref_set):
    ref_set = processing_ref_set
    ref_set.fail()

    assert ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_FAILED


def test_failed_from_done(done_ref_set):
    ref_set = done_ref_set
    ref_set.fail()

    assert ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_FAILED

def test_failed_from_failed(failed_ref_set):
    ref_set = failed_ref_set
    ref_set.fail()

    assert ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_FAILED

def test_reset_pending_from_pending(pending_ref_set):
    ref_set = pending_ref_set
    ref_set.reset_pending()

    assert ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_PENDING

def test_reset_pending_from_processing(processing_ref_set):
    ref_set = processing_ref_set
    ref_set.reset_pending()

    assert ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_PENDING

def test_reset_pending_from_failed(failed_ref_set):
    ref_set = failed_ref_set
    ref_set.reset_pending()

    assert ref_set.object_state == \
        ReferenceSet.STATE.LENS_CORRECTION_PENDING
