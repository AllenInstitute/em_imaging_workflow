from workflow_engine.strategies import execution_strategy
from rendermodules.registration.schemas import (
    RegisterSectionSchema
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
from at_em_imaging_workflow.strategies import (
    get_workflow_node_input_template
)
from django.conf import settings
import logging


class RegistrationStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'registration.registration_strategy')

    def get_input(self, chnk_assn, storage_directory, task):
        inp = get_workflow_node_input_template(
            task,
            name='Registration Input')

        em_mset = chnk_assn.section.montageset_set.first(
            ).emmontageset
        chnk = chnk_assn.chunk

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        registration_configuration=chnk.configurations.get(
            configuration_type='registration_configuration'
        ).json_object

        return RegisterSectionSchema().dump(inp).data
