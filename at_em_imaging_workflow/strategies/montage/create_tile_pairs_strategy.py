from workflow_engine.strategies import ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
from workflow_engine.models.configuration import Configuration
from rendermodules.pointmatch.schemas import TilePairClientParameters
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
import logging


class CreateTilePairsStrategy(ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'montage.create_tile_pairs_strategy')

    def get_input(self, em_mset, storage_directory, task):
        del storage_directory  # unused
        del task  # unused

        inp = Configuration.objects.get(
            name='Create Tile Pairs Input',
            configuration_type='strategy_config').json_object

        stack_names = \
            TwoDStackNameManager.create_tile_pairs_stacks(em_mset)

        inp['render'] = RenderStrategyUtils.render_input_dict(em_mset)

        inp['output_dir'] = em_mset.get_storage_directory()
        inp['baseStack'] = stack_names['baseStack']
        inp['stack'] = stack_names['stack']

        inp["minZ"] = em_mset.section.z_index
        inp["maxZ"] = em_mset.section.z_index

        return TilePairClientParameters().dump(inp)

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'tile_pair_file')
        self.set_well_known_file(
            results['tile_pair_file'],
            em_mset,
            em_mset.tile_pairs_file_description(),
            task)
