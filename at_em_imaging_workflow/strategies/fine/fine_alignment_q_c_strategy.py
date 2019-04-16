from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy


class FineAlignmentQCStrategy(InputConfigMixin, ExecutionStrategy):

    def get_input(self, enqueued_object, storage_directory, task):
        input_data = {}

        return input_data

    def on_finishing(self, enqueued_object, results, task):
        self.check_key(results, 'output_json')

        self.set_well_known_file(
            results['output_json'],
            enqueued_object,
            'description',
            task
        )
