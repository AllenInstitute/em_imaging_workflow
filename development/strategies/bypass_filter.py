from workflow_engine.strategies.wait_strategy \
    import WaitStrategy


class BypassFilter(WaitStrategy):

    def can_transition(self, em_mset):
        return em_mset.microscope.uid == 'temca3'

    def must_wait(self, em_mset):
        return False

