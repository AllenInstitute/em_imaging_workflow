from workflow_engine.strategies import WaitStrategy
from at_em_imaging_workflow.models import (
    Chunk,
    EMMontageSet
)
import itertools as it
import logging


class WaitForChunkAssignment(WaitStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.rough.'
        'wait_for_chunk_assignment'
    )
    QUEUE_NAME="Wait for Chunk Assignment"

    def transform_objects_for_queue(self, source_object):
        if type(source_object) == EMMontageSet:
            em_mset = source_object

            return [em_mset]
        elif type(source_object) == Chunk:
            chnk = source_object

            queued_montage_set_jobs = set(it.chain.from_iterable(
                m.jobs.filter(
                    workflow_node__job_queue__name=WaitForChunkAssignment.QUEUE_NAME,
                    run_state__name__in=[
                        'QUEUED',
                        'FAILED',
                        'FAILED_EXECUTION',
                        'SUCCESS'
                    ]
                )
                for m in chnk.em_montage_sets()
            ))

            queued_montage_sets = [
                j.enqueued_object for j in queued_montage_set_jobs
            ]

            return queued_montage_sets
        else:
            WaitForChunkAssignment._log.info(
                'unexpected object type'
            )

    def must_wait(self, em_mset):
        if em_mset.section.chunks.count() > 0:
            return False

        return True
