from workflow_engine.strategies import WaitStrategy
from at_em_imaging_workflow.models import (
    EMMontageSet,
    Load
)
import itertools as it
import logging


class WaitForZMapping(WaitStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies'
        '.montage.wait_for_z_mapping')
    QUEUE_NAME = "Wait for Z Mapping"

    def transform_objects_for_queue(self, source_object):
        enqueued_object_type = type(source_object)
        em_mset = None

        if enqueued_object_type == Load:
            load_object = source_object

            WaitForZMapping._log.info(
                'got load: {}'.format(load_object)
            )
        elif enqueued_object_type == EMMontageSet:
            em_mset = source_object
            load_object = em_mset.sample_holder.load

            if load_object.object_state != Load.STATE.LOAD_Z_MAPPED:
                WaitForZMapping._log.info(
                    'got unmapped montage set: {}'.format(em_mset)
                )

            return [em_mset]
        else:
            WaitForZMapping._log.warning(
                'Unexpected enqueued object type: %s',
                str(enqueued_object_type)
            )
            return []

        shared_load_montage_sets = EMMontageSet.objects.filter(
            sample_holder__load=load_object)

        queued_montage_set_jobs = set(it.chain.from_iterable(
            m.jobs.filter(
                workflow_node__job_queue__name=WaitForZMapping.QUEUE_NAME,
                run_state__name__in=[
                    'QUEUED',
                    'FAILED',
                    'FAILED_EXECUTION',
                    'SUCCESS'
                ]
            )
            for m in shared_load_montage_sets
        ))

        queued_montage_sets = set(
            j.enqueued_object for j in queued_montage_set_jobs
        )

        if em_mset is not None:
            queued_montage_sets.add(em_mset)

        WaitForZMapping._log.info(
            'Montage Sets to Wait on: {}'.format(queued_montage_sets)
        )

        return queued_montage_sets


    def must_wait(self, em_mset):
        if em_mset.sample_holder.load.object_state != Load.STATE.LOAD_Z_MAPPED:
            return True

        return False
