from workflow_engine.strategies.execution_strategy import ExecutionStrategy
from development.strategies.schemas.create_tile_pairs import input_dict
from rendermodules.pointmatch.schemas import \
    TilePairClientParameters
from django.conf import settings
import logging
import copy
from development.strategies \
    import RENDER_STACK_LENS_CORRECTED


class CreateRoughPairsStrategy(ExecutionStrategy):
    _log = logging.getLogger('development.strategies.create_rough_pairs_strategy')

    def get_input(self, chnk, storage_directory, task):
        inp = copy.deepcopy(input_dict)
    
        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['output_dir'] = chnk.get_storage_directory()
        inp['baseStack'] = RENDER_STACK_LENS_CORRECTED
        inp['stack'] = RENDER_STACK_LENS_CORRECTED

        min_z,max_z = chnk.z_range()
        inp["minZ"] = min_z
        inp["maxZ"] = max_z

        return TilePairClientParameters().dump(inp).data 

    def on_finishing(self, chnk, results, task):
        self.check_key(results, 'tile_pair_file')
        self.set_well_known_file(
            results['tile_pair_file'],
            chnk,
            chnk.tile_pairs_file_description(),
            task)
