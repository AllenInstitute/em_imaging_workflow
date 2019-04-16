from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
from rendermodules.fusion.schemas import RegisterSubvolumeParameters
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
from .fusion_input_generator import FusionInputGenerator, EnqueuedObject
import logging


class RegisterAdjacentStackStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.fusion.'
        'register_adjacent_stack_strategy')

    def get_input(self, chnk, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Register Adjacent Stack Input')

        fig = FusionInputGenerator(chnk)
        fig_json = fig.register_adjacent_output_json(EnqueuedObject(chnk))

        inp['render'] = RenderStrategyUtils.render_input_dict(chnk)

        inp['fig_json'] = fig_json

        stack_names = TwoDStackNameManager.register_adjacent_stacks(chnk)
        inp['stack_a'] = stack_names['stack_a']
        inp['stack_b'] = stack_names['stack_b']

        return RegisterSubvolumeParameters().dump(inp).data
