from workflow_engine.strategies.execution_strategy import ExecutionStrategy

class MoveRawMontageSetStrategy(ExecutionStrategy):

    #override if needed
    #set the data for the input file
    def get_input(self, em_mset, storage_directory, task):
        input_data = {}

        return input_data

    #override if needed
    #set the storage directory for an enqueued object
    #def get_storage_directory(self, base_storage_directory, job):
    #    enqueued_object = job.get_enqueued_object()
    #    return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
