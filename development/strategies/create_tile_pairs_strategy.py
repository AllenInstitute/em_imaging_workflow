from workflow_engine.strategies import execution_strategy
# from workflow_engine.models import *
# from development.models import *
from rendermodules.pointmatch.schemas import \
    TilePairClientParameters
from django.conf import settings
from os import listdir
import logging
import os

class CreateTilePairsStrategy(execution_strategy.ExecutionStrategy):
  _log = logging.getLogger('development.strategies.create_tile_pairs_strategy')

  default_input = {
    "render": {
        "host": "http://em-131fs",
        "port": 8998,
        "owner": "gayathri",
        "project": "MM2",
        "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
    },
    "minZ":1015,
    "maxZ":1022,
    "zNeighborDistance":0,
    "baseStack":"mm2_acquire_8bit_reimage",
    "stack":"mm2_acquire_8bit_reimage",
    "xyNeighborFactor": 0.9,
    "excludeCornerNeighbors":"true",
    "excludeSameLayerNeighbors":"false",
    "excludeCompletelyObscuredTiles":"true",
    "output_dir":"/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch/montageTilepairs"
  }

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    CreateTilePairsStrategy._log.info("get input")

    input = CreateTilePairsStrategy.default_input

    input['render']['host'] = settings.RENDER_SERVICE_URL
    input['render']['port'] = settings.RENDER_SERVICE_PORT
    input['render']['owner'] = settings.RENDER_SERVICE_USER
    input['render']['project'] = settings.RENDER_SERVICE_PROJECT
    input['render']['output_dir'] = '/example_data/scratch'

    input['stack'] = 'TEST_IMPORT_FROMMD'

    return TilePairClientParameters().dump(input).data 

  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, enqueued_object, results, task):
    CreateTilePairsStrategy._log.info("ON FINISHING")
    # self.check_key(results, 'output_json')
    # self.set_well_known_file(results['output_json'], enqueued_object, 'description', task)

  #override if needed
  #set the storage directory for an enqueued object
  #def get_storage_directory(self, base_storage_directory, job):
  #  enqueued_object = job.get_enqueued_object()
  #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
