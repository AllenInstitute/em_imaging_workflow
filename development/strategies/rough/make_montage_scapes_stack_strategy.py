from workflow_engine.strategies import execution_strategy
from rendermodules.dataimport.schemas \
    import MakeMontageScapeSectionStackParameters
from development.models.chunk_assignment import ChunkAssignment
from development.models.e_m_montage_set import EMMontageSet
from workflow_engine.models.configuration import Configuration
from development.strategies \
    import RENDER_STACK_SOLVED, RENDER_STACK_DOWNSAMPLED
from django.conf import settings
import logging


class MakeMontageScapesStackStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.models'
        '.make_montage_scapes_stack_strategy')

    def get_input(self, chunk_assignment, storage_directory, task):
        inp = Configuration.objects.get(
            name='Make Montage Scapes Input',
            configuration_type='strategy_config').json_object

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = \
            self.get_render_project_name(
                chunk_assignment)
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['minZ'] = chunk_assignment.section.z_index
        inp['maxZ'] = chunk_assignment.section.z_index

        # TODO: get most recent one.
        em_mset = EMMontageSet.objects.filter(
            section=chunk_assignment.section).first()

        inp['image_directory'] = em_mset.get_storage_directory(
            settings.LONG_TERM_BASE_FILE_PATH)

        # TODO: error reporting
        #downsample_config = em_mset.configurations.filter(
        #    configuration_type='downsample temp stack').first()

        inp['montage_stack'] = RENDER_STACK_SOLVED
        # downsample_config.json_object[
        #    'downsample_temp_stack']

        (z_start, z_end) = chunk_assignment.chunk.z_range()
        inp['output_stack'] = RENDER_STACK_DOWNSAMPLED

        return MakeMontageScapeSectionStackParameters().dump(inp).data

    def get_render_project_name(self, chunk_assignment):
        return chunk_assignment.section.specimen.uid

    def get_task_objects_for_queue(self, em_montage_set):
        return list(ChunkAssignment.objects.filter(
            section=em_montage_set.section))
