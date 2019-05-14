from workflow_engine.strategies import WaitStrategy
from at_em_imaging_workflow.models import (
    Chunk,
    EMMontageSet
)


class WaitForCompleteChunk(WaitStrategy):
    QUEUE_NAME='Wait for Lens Correction'

    def can_transition(self, enqueued_object, source_node=None):
        if type(enqueued_object) == Chunk:
            return True
        elif type(enqueued_object) == EMMontageSet:
            em_mset = enqueued_object

            if em_mset.section.chunks.filter(
                object_state=Chunk.STATE.CHUNK_INCOMPLETE
            ).count() > 0:
                return True

        return False

    def transform_objects_for_queue(self, source_object):
        if type(source_object) == EMMontageSet:
            em_mset = source_object

            return list(em_mset.section.chunks.all().filter(
                object_state=Chunk.STATE.CHUNK_INCOMPLETE))
        elif type(source_object) == Chunk:
            chnk = source_object

            return [ chnk ]
        else:
            WaitForCompleteChunk._log.warn(
                "unexpected enqueued object {}".format(str(source_object))
            )

            return []

    def must_wait(self, chnk):
        if chnk.is_complete():
            return False

        return True

