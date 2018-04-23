from workflow_engine.strategies import execution_strategy
from rendermodules.montage.schemas import SolveMontageSectionParameters
from development.strategies.schemas.two_d_montage_solver import input_dict
from django.conf import settings
import logging
from development.strategies \
    import RENDER_STACK_SOLVED, RENDER_STACK_LENS_CORRECTED


class TwoDMontageSolverStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.two_d_montage_solver_strategy')


    #override if needed
    #set the data for the input file
    def get_input(self, em_mset, storage_directory, task):
        TwoDMontageSolverStrategy._log.info("get input")

        inp = input_dict

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['source_collection']['service_host'] = \
            settings.RENDER_SERVICE_URL + ":" + settings.RENDER_SERVICE_PORT
        inp['source_collection']['baseURL'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + settings.RENDER_SERVICE_PORT + '/render-ws/v1'
        inp['source_collection']['owner'] = settings.RENDER_SERVICE_USER
        inp['source_collection']['project'] = em_mset.get_render_project_name()
        inp['source_collection']['renderbinPath'] = \
            settings.RENDER_CLIENT_SCRIPTS
        inp['source_collection']['stack'] = RENDER_STACK_LENS_CORRECTED

        inp['target_collection']['service_host'] = \
            settings.RENDER_SERVICE_URL + ":" + settings.RENDER_SERVICE_PORT
        inp['target_collection']['baseURL'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + settings.RENDER_SERVICE_PORT + '/render-ws/v1'
        inp['target_collection']['owner'] = settings.RENDER_SERVICE_USER
        inp['target_collection']['project'] = em_mset.get_render_project_name()
        inp['target_collection']['renderbinPath'] = \
            settings.RENDER_CLIENT_SCRIPTS
        inp['target_collection']['stack'] = RENDER_STACK_SOLVED

        inp['source_point_match_collection']['server'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + settings.RENDER_SERVICE_PORT + '/render-ws/v1'
        inp['source_point_match_collection']['owner'] = \
            settings.RENDER_SERVICE_USER
        inp['source_point_match_collection']['match_collection'] = \
            em_mset.get_point_collection_name()

        inp['first_section'] = em_mset.section.z_index
        inp['last_section'] = em_mset.section.z_index
        inp['solver_executable'] = self.get_solver_executable_path()

        task_dir = self.get_or_create_task_storage_directory(task)
        inp['temp_dir'] = task_dir

        # this needs to match mic scratch directory
        inp['solver_options']['dir_scratch'] = em_mset.get_storage_directory()

        return  SolveMontageSectionParameters().dump(inp).data

    def get_solver_executable_path(self):
        return settings.MONTAGE_SOLVER_BIN

