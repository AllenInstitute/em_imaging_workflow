from workflow_engine.strategies import WaitStrategy


class DefineChunksStrategy(WaitStrategy):

    def must_wait(self, load_object):
        # TODO: remain here until entire z range is accounted for
        return True
