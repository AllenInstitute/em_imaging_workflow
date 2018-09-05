from development.models import ReferenceSet
from workflow_engine.strategies.wait_strategy \
    import WaitStrategy


class WaitForLensCorrection(WaitStrategy):
    def must_wait(self, em_mset):
        # Use this to check if the reference set is available
        # return true if the state is correct
        ref_set = em_mset.reference_set
        
        if ref_set is None or \
            ReferenceSet.STATE.LENS_CORRECTION_DONE != \
                em_mset.reference_set.object_state:
            return True

        return False
