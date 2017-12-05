from workflow_engine.strategies import execution_strategy
from workflow_engine.models.job import Job
from workflow_engine.models.workflow_node import WorkflowNode

class MoveRawMontageSetStrategy(execution_strategy.ExecutionStrategy):

    #override if needed
    #set the data for the input file
    def get_input(self, enqueued_object, storage_directory, task):
        input_data = {}

        return input_data

    def on_finishing(self, ref_set, results, task):
        WorkflowNode.set_jobs_for_run(
            'Wait for Lens Correction')

    #override if needed
    #set the storage directory for an enqueued object
    #def get_storage_directory(self, base_storage_directory, job):
    #    enqueued_object = job.get_enqueued_object()
    #    return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
