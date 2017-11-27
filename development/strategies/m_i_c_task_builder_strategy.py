from workflow_engine.strategies import execution_strategy
from development.strategies.schemas.m_i_c_task_builder import input_dict
from rendermodules.intensity_correction.schemas import \
    MakeMedianParams 
from django.conf import settings
from os import listdir
import logging
import copy
import os

class MICTaskBuilderStrategy(execution_strategy.ExecutionStrategy):
  _log = logging.getLogger('development.strategies.m_i_c_task_builder_strategy')

  #override if needed
  #set the data for the input file
  def get_input(self, em_mset, storage_directory, task):
    '''
    Args:
        em_mset (EMMontageSet) the enqueued object
    '''
    MICTaskBuilderStrategy._log.info('MIC Task Builder')
    inp = copy.deepcopy(input_dict)

    inp['render']['host'] = settings.RENDER_SERVICE_URL
    inp['render']['port'] = settings.RENDER_SERVICE_PORT
    inp['render']['owner'] = settings.RENDER_SERVICE_USER
    inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
    inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
    inp['render']['output_dir'] = em_mset.storage_directory
    inp['input_stack'] = self.get_input_stack_name()
    inp['output_stack'] = self.get_output_stack_name()
    inp['minZ'] = em_mset.section.z_index
    inp['maxZ'] = em_mset.section.z_index

    return MakeMedianParams().dump(inp).data
    
  def get_input_stack_name(self):
    return settings.RENDER_STACK_NAME

  def get_output_stack_name(self):
    return settings.RENDER_STACK_NAME

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
