from workflow_engine.strategies import execution_strategy
from rendermodules.dataimport.schemas \
    import MakeMontageScapeSectionStackParameters
from development.strategies \
    import RENDER_STACK_SOLVED_PYTHON, RENDER_STACK_DOWNSAMPLED, \
    get_workflow_node_input_template

from django.conf import settings
import logging


class MakeMontageScapesStackStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.models'
        '.make_montage_scapes_stack_strategy')

    def get_input(self, em_mset, storage_directory, task):
        inp = get_workflow_node_input_template(task)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['set_new_z'] = True
        z_index = em_mset.section.z_index
        inp['minZ'] = z_index
        inp['maxZ'] = z_index
        z_mapping = em_mset.sample_holder.load.configurations.get(
            configuration_type='z_mapping').json_object
        inp['new_z_start'] = z_mapping[str(z_index)]

        inp['image_directory'] = em_mset.get_storage_directory(
            settings.LONG_TERM_BASE_FILE_PATH)

        if inp['montage_stack'] == '':
            inp['montage_stack'] = RENDER_STACK_SOLVED_PYTHON

        if inp['output_stack'] == '':
            inp['output_stack'] = RENDER_STACK_DOWNSAMPLED

        return MakeMontageScapeSectionStackParameters().dump(inp).data
