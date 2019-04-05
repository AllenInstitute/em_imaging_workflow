import itertools as it
from development.models import (
    ReferenceSet,
    EMMontageSet
)

from workflow_engine.strategies.wait_strategy import WaitStrategy


class WaitForLensCorrection(WaitStrategy):
    QUEUE_NAME='Wait for Lens Correction'

    def get_objects_for_queue(self, source_job):
        enqueued_object = source_job.enqueued_object
        enqueued_object_type = type(enqueued_object)
        em_mset = None

        if enqueued_object_type == ReferenceSet:
            reference_set = enqueued_object

            WaitForLensCorrection._log.info(
                'got Reference Set: {}'.format(reference_set)
            )
        elif enqueued_object_type == EMMontageSet:
            em_mset = enqueued_object
            reference_set = em_mset.reference_set

            if reference_set is None:
                WaitForLensCorrection._log.info(
                    'got Montage Set with no Reference: {}'.format(em_mset)
                )

                return [em_mset]
        else:
            WaitForLensCorrection._log.warn(
                'Unexpected enqueued object type: {}'.format(
                    enqueued_object_type
                )
            )
            return []

        shared_reference_montage_sets = \
            reference_set.emmontageset_set.all()

        queued_montage_set_jobs = set(it.chain.from_iterable(
            m.jobs.filter(
                workflow_node__job_queue__name=WaitForLensCorrection.QUEUE_NAME,
                run_state__name__in=[
                    'QUEUED',
                    'FAILED',
                    'FAILED_EXECUTION',
                    'SUCCESS'
                ]
            )
            for m in shared_reference_montage_sets
        ))

        queued_montage_sets = set(
            j.enqueued_object for j in queued_montage_set_jobs
        )

        if em_mset is not None:
            queued_montage_sets.add(em_mset)

        WaitForLensCorrection._log.info(
            'Montage Sets to Wait on: {}'.format(queued_montage_sets)
        )

        return queued_montage_sets


    def must_wait(self, em_mset):
        # Use this to check if the reference set is available
        # return true if the state is correct
        ref_set = em_mset.reference_set

        if ((ref_set is None) or
            (ReferenceSet.STATE.LENS_CORRECTION_DONE !=
             em_mset.reference_set.object_state)):
            WaitForLensCorrection._log.info("{} must wait".format(em_mset))
            return True

        WaitForLensCorrection._log.info("{} is not waiting".format(em_mset))
        return False

