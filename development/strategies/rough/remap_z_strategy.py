from workflow_engine.strategies import execution_strategy
from rendermodules.stack.schemas \
    import RemapZsParameters
from development.strategies \
    import RENDER_STACK_DOWNSAMPLED, \
    RENDER_STACK_DOWNSAMPLED_MAPPED, \
    get_workflow_node_input_template

from django.conf import settings
import logging


class RemapZStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.models'
        '.remap_z_strategy')

    def get_input(self, em_mset, storage_directory, task):
        inp = get_workflow_node_input_template(task)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['overwrite_zlayer'] = True
        inp['close_stack'] = False
        z_index = em_mset.section.z_index
        inp['zValues'] = [ z_index ]
        z_mapping = em_mset.sample_holder.load.configurations.get(
            configuration_type='z_mapping').json_object
        inp['new_zValues'] = z_mapping[str(z_index)]

        inp['input_stack'] = RENDER_STACK_DOWNSAMPLED
        inp['output_stack'] = RENDER_STACK_DOWNSAMPLED_MAPPED

        return RemapZsParameters().dump(inp).data
