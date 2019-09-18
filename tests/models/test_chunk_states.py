import pytest
from django_fsm import TransitionNotAllowed
from at_em_imaging_workflow.models import Chunk


@pytest.fixture
def incomplete_chunk():
    chnk = Chunk()

    return chnk


@pytest.fixture
def processing_chunk(incomplete_chunk):
    chnk = incomplete_chunk
    chnk.start_processing()

    return chnk

@pytest.fixture
def rough_qc_chunk(processing_chunk):
    chnk = processing_chunk
    chnk.finish_processing()

    return chnk

@pytest.fixture
def rough_qc_fail_chunk(rough_qc_chunk):
    chnk = rough_qc_chunk
    chnk.rough_qc_fail()

    return chnk

@pytest.fixture
def rough_qc_pass_chunk(rough_qc_chunk):
    chnk = rough_qc_chunk
    chnk.rough_qc_pass()

    return chnk

@pytest.fixture
def point_match_fail_chunk(rough_qc_pass_chunk):
    chnk = rough_qc_pass_chunk
    chnk.point_match_fail()

    return chnk

@pytest.fixture
def point_match_pass_chunk(rough_qc_pass_chunk):
    chnk = rough_qc_pass_chunk
    chnk.point_match_pass()

    return chnk

@pytest.fixture
def pending_fusion_chunk(point_match_pass_chunk):
    chnk = point_match_pass_chunk
    chnk.pending_fusion()

    return chnk

@pytest.fixture
def fusing_chunk(pending_fusion_chunk):
    chnk = pending_fusion_chunk
    chnk.start_fusion()

    return chnk

@pytest.fixture
def fusion_qc_chunk(fusing_chunk):
    chnk = fusing_chunk
    chnk.stop_fusion()

    return chnk

@pytest.fixture
def fusion_qc_failed_chunk(fusion_qc_chunk):
    chnk = fusion_qc_chunk
    chnk.fusion_qc_fail()

    return chnk

@pytest.fixture
def fusion_qc_passed_chunk(fusion_qc_chunk):
    chnk = fusion_qc_chunk
    chnk.fusion_qc_pass()

    return chnk

@pytest.fixture
def pending_render_chunk(fusion_qc_passed_chunk):
    chnk = fusion_qc_passed_chunk
    chnk.pending_render()

    return chnk

def test_pending_default(incomplete_chunk):
    assert incomplete_chunk.object_state == 'PENDING'


def test_start_processing(processing_chunk):
    assert processing_chunk.object_state == \
        Chunk.STATE.CHUNK_PROCESSING

def test_finish_processing(rough_qc_chunk):
    assert rough_qc_chunk.object_state == \
        Chunk.STATE.CHUNK_ROUGH_QC

def test_rough_qc_fail(rough_qc_fail_chunk):
    assert rough_qc_fail_chunk.object_state == \
        Chunk.STATE.CHUNK_ROUGH_QC_FAILED

def test_rough_qc_pass(rough_qc_pass_chunk):
    assert rough_qc_pass_chunk.object_state == \
        Chunk.STATE.CHUNK_ROUGH_QC_PASSED

def test_point_match_fail(point_match_fail_chunk):
    assert point_match_fail_chunk.object_state == \
        Chunk.STATE.CHUNK_POINT_MATCH_QC_FAILED

def test_point_match_pass(point_match_pass_chunk):
    assert point_match_pass_chunk.object_state == \
        Chunk.STATE.CHUNK_POINT_MATCH_QC_PASSED

def test_pending_fusion(pending_fusion_chunk):
    assert pending_fusion_chunk.object_state == \
        Chunk.STATE.CHUNK_PENDING_FUSION

def test_fusion(fusing_chunk):
    assert fusing_chunk.object_state == \
        Chunk.STATE.CHUNK_FUSING

def test_fusion_qc(fusion_qc_chunk):
    assert fusion_qc_chunk.object_state == \
        Chunk.STATE.CHUNK_FUSION_QC

def test_fusion_qc_failed(fusion_qc_failed_chunk):
    assert fusion_qc_failed_chunk.object_state == \
        Chunk.STATE.CHUNK_FUSION_QC_FAILED

def test_fusion_qc_passed(fusion_qc_passed_chunk):
    assert fusion_qc_passed_chunk.object_state == \
        Chunk.STATE.CHUNK_FUSION_QC_PASSED

def test_pending_render(pending_render_chunk):
    assert pending_render_chunk.object_state == \
        Chunk.STATE.CHUNK_PENDING_RENDER
