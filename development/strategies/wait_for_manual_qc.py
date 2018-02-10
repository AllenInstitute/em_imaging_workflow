from workflow_engine.strategies.wait_strategy \
    import WaitStrategy


class WaitForManualQc(WaitStrategy):
    def must_wait(self, em_mset):
        if em_mset.workflow_state is not None and \
            'MONTAGE_QC_PASSED' != em_mset.workflow_state:
            return False

        return True
