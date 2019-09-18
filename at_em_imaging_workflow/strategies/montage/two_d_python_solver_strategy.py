from workflow_engine.strategies import execution_strategy
from workflow_engine.models.configuration import Configuration
from at_em_imaging_workflow.models import EMMontageSet
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
from django.conf import settings
from django_fsm import can_proceed
import logging


class TwoDPythonSolverStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies'
        '.montage.two_d_python_solver_strategy')

    def can_transition(self, em_mset, node):
        return True

    def get_input(self, em_mset, storage_directory, task):
        TwoDPythonSolverStrategy._log.info("get input")

        inp = Configuration.objects.get(
            name='2D Montage Python Solver Input',
            configuration_type='strategy_config').json_object

        stack_names = \
            TwoDStackNameManager.two_d_python_solver_stacks(em_mset)

        inp['pointmatch']['host'] = settings.RENDER_SERVICE_URL
        inp['pointmatch']['port'] = settings.RENDER_SERVICE_PORT
        inp['pointmatch']['owner'] = settings.RENDER_SERVICE_USER
        inp['pointmatch']['project'] = em_mset.get_render_project_name()
        inp['pointmatch']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['pointmatch']['name'] = em_mset.get_point_collection_name()
        inp['pointmatch']['db_interface'] = 'render'

        inp['input_stack']['host'] = settings.RENDER_SERVICE_URL
        inp['input_stack']['port'] = settings.RENDER_SERVICE_PORT
        inp['input_stack']['owner'] = settings.RENDER_SERVICE_USER
        inp['input_stack']['project'] = em_mset.get_render_project_name()
        inp['input_stack']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['input_stack']['name'] = stack_names['input_stack']
        inp['input_stack']['db_interface'] = 'render'

        inp['output_stack']['host'] = settings.RENDER_SERVICE_URL
        inp['output_stack']['port'] = settings.RENDER_SERVICE_PORT
        inp['output_stack']['owner'] = settings.RENDER_SERVICE_USER
        inp['output_stack']['project'] = em_mset.get_render_project_name()
        inp['output_stack']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['output_stack']['name'] = stack_names['output_stack']
        inp['output_stack']['db_interface'] = 'render'

        inp['first_section'] = em_mset.section.z_index
        inp['last_section'] = em_mset.section.z_index
        inp['solve_type'] = 'montage'
        inp['close_stack'] = False
        
        # TODO: remove this in on_finishing() - for fine alignment
        # won't write anything in rough or montage
        task_dir = self.get_or_create_task_storage_directory(task)
        inp['hdf5_options']['output_dir'] = task_dir

        redo_cfg = em_mset.get_redo_parameters()

        if ('transformation' in redo_cfg and
            redo_cfg['transformation'] is not None):
            inp['transformation'] = redo_cfg['transformation']

        if ('poly_order' in redo_cfg and
            redo_cfg['poly_order'] is not None):
            inp['poly_order'] = redo_cfg['poly_order']

        if ('poly_factors' in redo_cfg and
            redo_cfg['poly_factors'] is not None):
            inp['regularization']['poly_factors'] = redo_cfg['poly_factors']

        if ('default_lambda' in redo_cfg and
            redo_cfg['default_lambda'] is not None):
            inp['regularization']['default_lambda'] = \
                redo_cfg['default_lambda']

        return EMA_Schema().dump(inp).data

    def on_finishing(self, em_mset, results, task):
        if can_proceed(em_mset.finish_processing):
            em_mset.finish_processing()
            em_mset.save()
        elif em_mset.object_state == EMMontageSet.STATE.EM_MONTAGE_SET_QC_PASSED:
            TwoDPythonSolverStrategy._log.warning(
                'Unexpected state transition - remaining in QC Passed'
            )
        else:
            em_mset.finish_processing()  # expected to throw an exception
            em_mset.save()

try:
    from EMaligner.schemas import EMA_Schema
except:
    TwoDPythonSolverStrategy._log.warning('Could not import EMA_Schema')
