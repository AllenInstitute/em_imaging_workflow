from workflow_engine.strategies import execution_strategy
from rendermodules.dataimport.schemas \
    import MakeMontageScapeSectionStackParameters
from development.strategies import get_workflow_node_input_template
from at_em_imaging_workflow.two_d_stack_name_manager \
    import TwoDStackNameManager

from django.conf import settings
import logging


class MakeMontageScapesStackStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.models'
        '.make_montage_scapes_stack_strategy')

    def get_objects_for_queue(self, job):
        em_mset = job.enqueued_object

        if em_mset.microscope.uid == 'temca3':
            return [ em_mset ]
        else:
            return []

    def get_input(self, em_mset, storage_directory, task):
        inp = get_workflow_node_input_template(task)

        stack_names = \
            TwoDStackNameManager.make_montage_scapes_stacks(em_mset)

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

        inp['montage_stack'] = stack_names['montage_stack']

        inp['output_stack'] = stack_names['output_stack']

        return MakeMontageScapeSectionStackParameters().dump(inp).data
