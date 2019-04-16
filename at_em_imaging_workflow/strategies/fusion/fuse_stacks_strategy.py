from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from rendermodules.fusion.schemas import (
    FuseStacksParameters
)
from at_em_imaging_workflow.strategies.rough.solve_rough_alignment_strategy import (
    SolveRoughAlignmentStrategy
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
from django.conf import settings
import logging


class FuseStacksStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'fusion.fuse_stacks_strategy')

    def get_input(self, chnk, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Fuse Stacks Input')

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        volume_configuration=chnk.rendered_volume.configurations.get(
            configuration_type='rendered_volume_configuration'
        ).json_object

        inp['stacks'] = volume_configuration['stacks']

        return FuseStacksParameters().dump(inp).data
