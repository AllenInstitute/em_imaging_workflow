from workflow_engine.strategies.wait_strategy \
    import WaitStrategy


class WaitForLensCorrection(WaitStrategy):
    def must_wait(self, em_mset):
        # Use this to check if the reference set is available
        # return true if the state is correct
        if 'STOP' == em_mset.uid:
            return True

        return False