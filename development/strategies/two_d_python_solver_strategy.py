from workflow_engine.strategies import execution_strategy
from workflow_engine.models.configuration import Configuration
from django.core.exceptions import ObjectDoesNotExist
from at_em_imaging_workflow.two_d_stack_name_manager \
    import TwoDStackNameManager
from django.conf import settings
import logging


# TODO - do for rough alignment also
class TwoDPythonSolverStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.two_d_python_solver_strategy')

    #override if needed
    #set the data for the input file
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

        if em_mset.object_state == 'REDO_SOLVER':
            inp['regularization']['default_lambda'] = \
                em_mset.get_em_2d_solver_lambda(5.0)

        return EMA_Schema().dump(inp).data

    def on_finishing(self, em_mset, results, task):
        em_mset.finish_processing()
        em_mset.save()

    def get_default_lambda(
        self, em_mset, initial_default_lambda):
        default_lambda = 5.0

        cfg, _ = em_mset.configurations.get_or_create(
            configuration_type='point_match_parameters',
            defaults = {
                'name': 'point match params for {}'.format(
                    str(em_mset.id)),
            }
        )

        try:
            config = em_mset.configurations.get(
                configuration_type='point_match_parameters')
        except ObjectDoesNotExist:
            updated_state = {
                'default_lambda': initial_default_lambda
            }
            config = Configuration(
                content_object=em_mset,
                name='point match params for {}'.format(str(em_mset)),
                configuration_type='point_match_parameters',
                json_object=updated_state)

        default_lambda = 5.0
        config.json_object['default_lambda'] = default_lambda
        config.save()

        return default_lambda


try:
    from EMaligner.schemas import EMA_Schema
except:
    TwoDPythonSolverStrategy._log.warn('Could not import EMA_Schema')
