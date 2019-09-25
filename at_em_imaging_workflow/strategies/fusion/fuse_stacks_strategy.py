from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
# from rendermodules.fusion.schemas import (
#     FuseStacksParameters
# )
import logging


class FuseStacksStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'fusion.fuse_stacks_strategy')

    def get_input(self, chnk, storage_directory, task):
        pass
#         inp = self.get_workflow_node_input_template(
#             task,
#             name='Fuse Stacks Input')
# 
#         inp['render'] = RenderStrategyUtils.render_input_dict(chnk)
# 
#         volume_configuration=chnk.rendered_volume.configurations.get(
#             configuration_type='rendered_volume_configuration'
#         ).json_object
# 
#         inp['stacks'] = volume_configuration['stacks']
#
#        return FuseStacksParameters().dump(inp).data
