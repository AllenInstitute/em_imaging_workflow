from workflow_engine.strategies import WaitStrategy
from at_em_imaging_workflow.models import (
    Chunk,
    ChunkAssignment,
    EMMontageSet
)
import itertools as it


class WaitForChunkAssignment(WaitStrategy):
    QUEUE_NAME='Wait for Chunk Assignment'

    def can_transition(self, em_mset, source_node=None):
        if em_mset.section.chunks.count() > 0:
            return True

        return False

    def get_objects_for_queue(self, source_job):
        em_mset = source_job.enqueued_object

        return [em_mset]

    def must_wait(self, em_mset):
        # Use this to check if the reference set is available
        # return true if the state is correct
        return True
