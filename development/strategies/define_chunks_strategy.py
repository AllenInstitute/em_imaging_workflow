from development.models.chunk import Chunk
from workflow_engine.strategies.wait_strategy \
    import WaitStrategy


class DefineChunksStrategy(WaitStrategy):

    def must_wait(self, em_mset):
        chnks = Chunk.assign_montage_set_to_chunks(em_mset)

        trigger_next_queue = False

        # TODO: need to enqueue the complete objects
        for c in chnks:
            if c.is_complete():
                trigger_next_queue = True

        return trigger_next_queue