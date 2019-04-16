from workflow_engine.strategies import WaitStrategy
from at_em_imaging_workflow.models import EMMontageSet, Load

class LoadZMappingStrategy(WaitStrategy):

    def can_transition(self, load, source_node=None):
        if load.object_state == Load.STATE.LOAD_PENDING:
            return True

        return False

    def get_objects_for_queue(self, source_job):
        enqueued_object = source_job.enqueued_object

        if type(enqueued_object) is EMMontageSet:
            em_mset = source_job.enqueued_object
            load = em_mset.sample_holder.load

            return [load]
        else:
            return []

    def must_wait(self, load):
        return True