from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from rendermodules.fusion.schemas import (
    RegisterSubvolumeParameters
)
from at_em_imaging_workflow.strategies.rough.solve_rough_alignment_strategy import (
    SolveRoughAlignmentStrategy
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
from django.conf import settings
import logging


class RegisterAdjacentStackStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.fusion.'
        'register_adjacent_stack_strategy')

    def get_input(self, chnk, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Register Adjacent Stack Input')

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        stack_names = \
            TwoDStackNameManager.register_adjacent_stacks(chnk)

        inp['stack_a'] = stack_names['stack_a']
        inp['stack_b'] = stack_names['stack_b']

        return RegisterSubvolumeParameters().dump(inp).data
