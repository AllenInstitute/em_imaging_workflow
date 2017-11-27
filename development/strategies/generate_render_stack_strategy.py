from workflow_engine.strategies import execution_strategy
from development.strategies.schemas.generate_render_stack import input_dict
from rendermodules.dataimport.schemas import \
    GenerateEMTileSpecsParameters
from django.conf import settings
from os import listdir
import copy
import logging
import os

class GenerateRenderStackStrategy(execution_strategy.ExecutionStrategy):
  _log = logging.getLogger(
      'development.strategies.ingest_generate_render_stack_strategy')

  #override if needed
  #set the data for the input file
  def get_input(self, em_set, storage_directory, task):
    '''
    Args:
        em_set (EMMontageSet) the enqueued object
    '''
    GenerateRenderStackStrategy._log.info(
        'ingest/generate render stack')
    inp = copy.deepcopy(input_dict)

    inp['render']['host'] = settings.RENDER_SERVICE_URL
    inp['render']['port'] = settings.RENDER_SERVICE_PORT
    inp['render']['owner'] = settings.RENDER_SERVICE_USER
    inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
    inp['stack'] = self.get_stack_name(em_set)
    inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
    inp['metafile'] = em_set.metafile
    inp['close_stack'] = False
    inp['z_index'] = self.get_z_index(em_set)
 
    return GenerateEMTileSpecsParameters().dump(inp).data

  def get_z_index(self, em_set):
      return em_set.section.z_index

  def get_stack_name(self, em_set):
      return settings.RENDER_STACK_NAME

  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, enqueued_object, results, task):
    # self.check_key(results, 'output_json')
    # self.set_well_known_file(results['output_json'],
    #                          enqueued_object,
    #                          'description',
    #                          task)
    pass

  #override if needed
  #set the storage directory for an enqueued object
  #def get_storage_directory(self, base_storage_directory, job):
  #  enqueued_object = job.get_enqueued_object()
  #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
