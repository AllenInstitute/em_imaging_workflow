from workflow_engine.strategies import execution_strategy
# from workflow_engine.models import *
# from development.models import *
from rendermodules.intensity_correction.schemas import \
    MultIntensityCorrParams
from django.conf import settings
import logging

class MICTasksStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger('development.strategies.m_i_c_tasks_strategy')

    default_input = {
      "render": {
          "host": "ibs-forrestc-ux1",
          "port": 8080,
          "owner": "M246930_Scnn1a",
          "project": "M246930_Scnn1a_4",
          "client_scripts": "/var/www/render/render-ws-java-client/src/main/scripts"
      },
      "input_stack": "Acquisition_DAPI_1",
      "correction_stack": "Median_TEST_DAPI_1",
      "output_stack": "Flatfield_TEST_DAPI_1",
      "output_directory": "/nas/data/M246930_Scnn1a_4/processed/FlatfieldTEST",
      "z_index": 102,
      "pool_size": 20
    }

    #override if needed
    #set the data for the input file
    def get_input(self, enqueued_object, storage_directory, task):
        '''
        Args:
            enqueued_object (EMMontageSet) 
        '''
        MICTasksStrategy._log.info('MIC Tasks')
        inp = MICTasksStrategy.default_input

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['render']['output_dir'] = '/example_data/scratch'

        inp['stack'] = 'test_LC'

        return MultIntensityCorrParams().dump(inp).data

    #override if needed
    #called after the execution finishes
    #process and save results to the database
    def on_finishing(self, enqueued_object, results, task):
        # self.check_key(results, 'output_json')
        # self.set_well_known_file(results['output_json'], enqueued_object, 'description', task)
        pass

    #override if needed
    #set the storage directory for an enqueued object
    #def get_storage_directory(self, base_storage_directory, job):
    #  enqueued_object = job.get_enqueued_object()
    #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
