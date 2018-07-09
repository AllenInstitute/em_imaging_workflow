from workflow_engine.strategies import execution_strategy
from rendermodules.dataimport.schemas \
    import MakeMontageScapeSectionStackParameters
from workflow_engine.models.configuration import Configuration
from development.strategies \
    import RENDER_STACK_SOLVED_PYTHON, RENDER_STACK_DOWNSAMPLED
from django.conf import settings
import logging


class MakeMontageScapesStackStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.models'
        '.make_montage_scapes_stack_strategy')

    def get_input(self, em_mset, storage_directory, task):
        inp = Configuration.objects.get(
            name='Make Montage Scapes Input',
            configuration_type='strategy_config').json_object

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['minZ'] = em_mset.section.z_index
        inp['maxZ'] = em_mset.section.z_index

        inp['image_directory'] = em_mset.get_storage_directory(
            settings.LONG_TERM_BASE_FILE_PATH)

        inp['montage_stack'] = RENDER_STACK_SOLVED_PYTHON

        inp['output_stack'] = RENDER_STACK_DOWNSAMPLED

        return MakeMontageScapeSectionStackParameters().dump(inp).data

    def get_render_project_name(self, chunk_assignment):
        return chunk_assignment.section.specimen.uid
