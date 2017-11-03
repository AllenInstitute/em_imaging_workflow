from workflow_engine.strategies import execution_strategy
#from workflow_engine.models import *
#from development.models import *
from rendermodules.dataimport.schemas import \
    GenerateEMTileSpecsParameters
from django.conf import settings
from os import listdir
import logging
import os

class IngestGenerateRenderStackStrategy(execution_strategy.ExecutionStrategy):
  _log = logging.getLogger(
      'development.strategies.ingest_generate_render_stack_strategy')
  default_input = {
    "render": {
        "host": "em-131fs",
        "port": 8080,
        "owner": "russelt",
        "project": "RENDERAPI_TEST",
        "client_scripts": (
            "/allen/programs/celltypes/workgroups/"
            "em-connectomics/russelt/render_mc.old/render-ws-java-client/"
            "src/main/scripts")},
    "metafile": "/allen/programs/celltypes/workgroups/em-connectomics/data/workflow_test_sqmm/001050/0/_metadata_20170829130146_295434_5LC_0064_01_redo_001050_0_.json",
    "stack": "TEST_IMPORT_FROMMD",
    "overwrite_zlayer": True,
    "pool_size": 10,
    "close_stack": True,
    "z_index": 1
  }

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    '''
    Args:
        enqueued_object (EMMontageSet) assuming this based on project_path
    '''
    IngestGenerateRenderStackStrategy._log.info(
        'ingest/generate render stack')
    input = IngestGenerateRenderStackStrategy.default_input

    input['render']['host'] = settings.RENDER_SERVICE_URL
    input['render']['port'] = settings.RENDER_SERVICE_PORT
    input['render']['owner'] = settings.RENDER_SERVICE_USER
    input['render']['project'] = settings.RENDER_SERVICE_PROJECT
    input['metafile'] = \
        os.path.join(
            '/allen/aibs/pipeline/image_processing/volume_assembly',
            'dataimport_test_data',
            '_metadata_20170829130146_295434_5LC_0064_01_redo_001050_0_.json')
    #     os.path.join(
    #         '/allen/aibs/pipeline/image_processing/volume_assembly',
    #         'dataimport_test_data',
    #         '_metadata_20170829130146_295434_5LC_0064_01_redo_001050_0_.json')
 
    return GenerateEMTileSpecsParameters().dump(input).data

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
