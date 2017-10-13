from workflow_engine.strategies import execution_strategy
# from workflow_engine.models import *
# from development.models import *
from rendermodules.intensity_correction.schemas import \
    MakeMedianParams 
from django.conf import settings
from os import listdir
import logging
import os

class ATMICTaskBuilderStrategy(execution_strategy.ExecutionStrategy):
  _log = logging.getLogger('development.strategies.at_m_i_c_task_builder_strategy')

  default_input = {
    "render": {
        "host": "ibs-forrestc-ux1",
        "port": 8080,
        "owner": "M246930_Scnn1a",
        "project": "M246930_Scnn1a_4",
        "client_scripts": "/var/www/render/render-ws-java-client/src/main/scripts"
    },
    "input_stack": "Acquisition_DAPI_1",
    "file_prefix": "Median",
    "output_stack": "Median_TEST_DAPI_1",
    "output_directory": "/nas/data/M246930_Scnn1a_4/processed/Medians",
    "minZ": 100,
    "maxZ": 103,
    "pool_size": 20
  }

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    '''
    Args:
        enqueued_object (EMMontageSet) 
    '''
    ATMICTaskBuilderStrategy._log.info('MIC Task Builder')
    input = ATMICTaskBuilderStrategy.default_input

    return MakeMedianParams().dump(input).data
    

  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, enqueued_object, results, task):

    self.check_key(results, 'output_json')

    self.set_well_known_file(results['output_json'], enqueued_object, 'description', task)

  #override if needed
  #set the storage directory for an enqueued object
  #def get_storage_directory(self, base_storage_directory, job):
  #  enqueued_object = job.get_enqueued_object()
  #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
