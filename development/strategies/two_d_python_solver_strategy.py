from workflow_engine.strategies import execution_strategy
from workflow_engine.models.configuration import Configuration
from development.strategies \
    import RENDER_STACK_LENS_CORRECTED, RENDER_STACK_SOLVED_PYTHON
from django.conf import settings
import logging  


# TODO - do for rouch alignment also
class TwoDPythonSolverStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.python_solver_strategy')

    #override if needed
    #set the data for the input file
    def get_input(self, em_mset, storage_directory, task):
        TwoDPythonSolverStrategy._log.info("get input")

        inp = Configuration.objects.get(
            name='2D Montage Python Solver Input',
            configuration_type='strategy_config').json_object

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
        inp['input_stack']['name'] = RENDER_STACK_LENS_CORRECTED
        inp['input_stack']['db_interface'] = 'render'

        inp['output_stack']['host'] = settings.RENDER_SERVICE_URL
        inp['output_stack']['port'] = settings.RENDER_SERVICE_PORT
        inp['output_stack']['owner'] = settings.RENDER_SERVICE_USER
        inp['output_stack']['project'] = em_mset.get_render_project_name()
        inp['output_stack']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['output_stack']['name'] = RENDER_STACK_SOLVED_PYTHON
        inp['output_stack']['db_interface'] = 'render'

        inp['first_section'] = em_mset.section.z_index
        inp['last_section'] = em_mset.section.z_index
        inp['solve_type'] = 'montage'  # TODO: also do a rough version
        inp['close_stack'] = False
        
        # TODO: remove this in on_finishing() - for fine alignment
        # won't write anything in rough or montage
        task_dir = self.get_or_create_task_storage_directory(task)
        inp['hdf5_options']['output_dir'] = task_dir

        return EMA_Schema().dump(inp).data


try:
    from EMaligner.EM_aligner_python_schema import EMA_Schema
except:
    TwoDPythonSolverStrategy._log.warn('Could not import EMA_Schema')
