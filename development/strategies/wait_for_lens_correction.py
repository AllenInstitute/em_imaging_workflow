from workflow_engine.strategies.manual_strategy \
    import ManualStrategy
import logging


class WaitForLensCorrection(ManualStrategy):
    _log = logging.getLogger(
        'development.strategies.wait_for_lens_correction')

    def task_finished(self, task):
        # enqueued_object = task.get_enqueued_object()
        return False

    def on_running(self, task):
        pass

    def on_finishing(self, enqueued_object, results, task):
        # Use this to update the state
        pass

