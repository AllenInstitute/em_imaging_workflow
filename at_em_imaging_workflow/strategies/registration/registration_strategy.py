from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
from rendermodules.registration.schemas import RegisterSectionSchema
import logging


class RegistrationStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'registration.registration_strategy')

    def get_input(self, chnk_assn, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Registration Input')

        em_mset = chnk_assn.section.montageset_set.first(
            ).emmontageset
        chnk = chnk_assn.chunk

        inp['render'] = RenderStrategyUtils.render_input_dict(chnk)

        registration_configuration=chnk.configurations.get(
            configuration_type='registration_configuration'
        ).json_object

        return RegisterSectionSchema().dump(inp).data
