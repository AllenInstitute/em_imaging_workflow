from at_em_imaging_workflow.models import Chunk
from workflow_engine.strategies import WaitStrategy


class DefineChunksStrategy(WaitStrategy):
    def get_objects_for_queue(self, source_job):
        em_mset = source_job.enqueued_object

        assigned_chunks = Chunk.assign_to_chunks(em_mset)

        return assigned_chunks

    def must_wait(self, chnk):
        return not chnk.is_complete()
