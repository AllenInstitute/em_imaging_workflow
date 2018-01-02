from workflow_engine.strategies.execution_strategy import ExecutionStrategy
from development.strategies.schemas.create_tile_pairs import input_dict
from rendermodules.pointmatch.schemas import \
    TilePairClientParameters
from django.conf import settings
import logging
import copy

class CreateTilePairsStrategy(ExecutionStrategy):
    _log = logging.getLogger('development.strategies.create_tile_pairs_strategy')

    def get_input(self, em_mset, storage_directory, task):
        CreateTilePairsStrategy._log.info("get input")

        inp = copy.deepcopy(input_dict)
    
        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['output_dir'] = self.get_or_create_task_storage_directory(task)
        inp['baseStack'] = em_mset.render_stack_name()
        inp['stack'] = em_mset.render_stack_name()

        inp["minZ"] = em_mset.section.z_index
        inp["maxZ"] = em_mset.section.z_index

        return TilePairClientParameters().dump(inp).data 

    def on_finishing(self, em_mset, results, task):
        CreateTilePairsStrategy._log.info("ON FINISHING")
        self.check_key(results, 'tile_pair_file')
        self.set_well_known_file(
            results['tile_pair_file'],
            em_mset,
            em_mset.tile_pairs_file_description(),
            task)

    #override if needed
    #set the storage directory for an enqueued object
    #def get_storage_directory(self, base_storage_directory, job):
    #  enqueued_object = job.get_enqueued_object()
    #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
