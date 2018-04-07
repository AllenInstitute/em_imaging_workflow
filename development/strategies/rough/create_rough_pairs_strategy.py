from workflow_engine.strategies.execution_strategy import ExecutionStrategy
from development.strategies.schemas.create_tile_pairs import input_dict
from rendermodules.pointmatch.schemas import \
    TilePairClientParameters
from django.conf import settings
import logging
import copy
from development.strategies.chmod_strategy import ChmodStrategy
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

        inp["minZ"] = chnk.section.z_index
        inp["maxZ"] = chnk.section.z_index

        return TilePairClientParameters().dump(inp).data 

    def on_finishing(self, chnk, results, task):
        self.check_key(results, 'tile_pair_file')
        self.set_well_known_file(
            results['tile_pair_file'],
            chnk,
            chnk.tile_pairs_file_description(),
            task)
        #chmod_directory(chnk.get_storage_directory())
        ChmodStrategy.add_chmod_dir(
            chnk, chnk.get_storage_directory())
        ChmodStrategy.add_chmod_file(
            chnk, chnk.get_storage_directory())
        ChmodStrategy.enqueue_montage(chnk)
