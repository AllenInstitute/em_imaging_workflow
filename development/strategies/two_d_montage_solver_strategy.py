from workflow_engine.strategies import execution_strategy
from rendermodules.montage.schemas import SolveMontageSectionParameters
from development.strategies.schemas.two_d_montage_solver import input_dict
from django.conf import settings
import logging
import os


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
        inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['source_collection']['service_host'] = \
            settings.RENDER_SERVICE_URL + ":" + settings.RENDER_SERVICE_PORT
        inp['source_collection']['baseURL'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + settings.RENDER_SERVICE_PORT + '/render-ws/v1'
        inp['source_collection']['owner'] = settings.RENDER_SERVICE_USER
        inp['source_collection']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['source_collection']['renderbinPath'] = \
            settings.RENDER_CLIENT_SCRIPTS
        inp['source_collection']['stack'] = self.get_input_stack_name()

        inp['target_collection']['service_host'] = \
            settings.RENDER_SERVICE_URL + ":" + settings.RENDER_SERVICE_PORT
        inp['target_collection']['baseURL'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + settings.RENDER_SERVICE_PORT + '/render-ws/v1'
        inp['target_collection']['owner'] = settings.RENDER_SERVICE_USER
        inp['target_collection']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['target_collection']['renderbinPath'] = \
            settings.RENDER_CLIENT_SCRIPTS
        inp['target_collection']['stack'] = self.get_output_stack_name()

        inp['source_point_match_collection']['server'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + settings.RENDER_SERVICE_PORT + '/render-ws/v1'
        inp['source_point_match_collection']['owner'] = \
            settings.RENDER_SERVICE_USER
        inp['source_point_match_collection']['match_collection'] = \
            self.get_collection_name()

        inp['z_value'] = em_mset.section.z_index
        inp['solver_executable'] = self.get_solver_executable_path()

        task_dir = self.get_or_create_task_storage_directory(task)
        inp['temp_dir'] = task_dir
        inp['dir_scratch'] = task_dir
        inp['renderer_client'] = os.path.join(settings.RENDER_CLIENT_SCRIPTS,
                                              'render.sh')

        return  SolveMontageSectionParameters().dump(inp).data

    def get_input_stack_name(self):
        return settings.RENDER_STACK_NAME

    def get_output_stack_name(self):
        return settings.RENDER_STACK_NAME

    def get_collection_name(self):
        return 'default_point_matches'

    def get_solver_executable_path(self):
        return settings.MONTAGE_SOLVER_BIN

    #override if needed
    #called after the execution finishes
    #process and save results to the database
    def on_finishing(self, enqueued_object, results, task):
        pass
