from workflow_engine.strategies.execution_strategy import ExecutionStrategy
from development.strategies.schemas.create_tile_pairs import input_dict
from rendermodules.pointmatch.schemas import \
    TilePairClientParameters
from django.conf import settings
import logging
import copy
from development.strategies \
    import RENDER_STACK_LENS_CORRECTED
from development.strategies.chmod_directories \
    import chmod_directory


class CreateTilePairsStrategy(ExecutionStrategy):
    _log = logging.getLogger('development.strategies.create_tile_pairs_strategy')

    def get_input(self, em_mset, storage_directory, task):
        inp = copy.deepcopy(input_dict)
    
        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['output_dir'] = em_mset.get_storage_directory()
        inp['baseStack'] = RENDER_STACK_LENS_CORRECTED
        inp['stack'] = RENDER_STACK_LENS_CORRECTED

        inp["minZ"] = em_mset.section.z_index
        inp["maxZ"] = em_mset.section.z_index

        return TilePairClientParameters().dump(inp).data 

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'tile_pair_file')
        self.set_well_known_file(
            results['tile_pair_file'],
            em_mset,
            em_mset.tile_pairs_file_description(),
            task)
        chmod_directory(em_mset.get_storage_directory())
