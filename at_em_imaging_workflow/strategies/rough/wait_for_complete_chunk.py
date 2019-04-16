from workflow_engine.strategies import WaitStrategy
from at_em_imaging_workflow.models import (
    Chunk,
    ChunkAssignment,
    EMMontageSet
)
import itertools as it


class WaitForCompleteChunk(WaitStrategy):
    QUEUE_NAME='Wait for Lens Correction'

    def can_transition(self, chnk, source_node=None):
        # TODO: calculate if chunk is complete

        return False

    def get_objects_for_queue(self, source_job):
        em_mset = source_job.enqueued_object

        return list(em_mset.section.chunks.all().filter(
            object_state=Chunk.STATE.CHUNK_INCOMPLETE))

    def must_wait(self, em_mset):
        # Use this to check if the reference set is available
        # return true if the state is correct
        return True

