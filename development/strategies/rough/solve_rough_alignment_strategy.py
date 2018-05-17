from workflow_engine.strategies.execution_strategy \
    import ExecutionStrategy
from rendermodules.rough_align.schemas \
    import SolveRoughAlignmentParameters
from workflow_engine.models.configuration import Configuration
from development.strategies \
    import RENDER_STACK_MONTAGE_SCAPES_STACK, RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE
from django.conf import settings


class SolveRoughAlignmentStrategy(ExecutionStrategy):

    def get_input(self, chnk, storage_directory, task):
        inp = Configuration.objects.get(
            name='Rough Alignment Solver Input',
            configuration_type='strategy_config').json_object

        (z_start, z_end) = chnk.z_range()

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['source_collection']['service_host'] = \
            settings.RENDER_SERVICE_URL + ":" + str(settings.RENDER_SERVICE_PORT)
        inp['source_collection']['baseURL'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + str(settings.RENDER_SERVICE_PORT) + '/render-ws/v1'
        inp['source_collection']['owner'] = settings.RENDER_SERVICE_USER
        inp['source_collection']['project'] = chnk.get_render_project_name()
        inp['source_collection']['renderbinPath'] = \
            settings.RENDER_CLIENT_SCRIPTS

        inp['source_collection']['stack'] = \
            RENDER_STACK_MONTAGE_SCAPES_STACK % (z_start, z_end)

        inp['target_collection']['service_host'] = \
            settings.RENDER_SERVICE_URL + ":" + str(settings.RENDER_SERVICE_PORT)
        inp['target_collection']['baseURL'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + str(settings.RENDER_SERVICE_PORT) + '/render-ws/v1'
        inp['target_collection']['owner'] = settings.RENDER_SERVICE_USER
        inp['target_collection']['project'] = chnk.get_render_project_name()
        inp['target_collection']['renderbinPath'] = \
            settings.RENDER_CLIENT_SCRIPTS
        inp['target_collection']['stack'] = \
            RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE % (z_start, z_end)

        inp['source_point_match_collection']['server'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + str(settings.RENDER_SERVICE_PORT) + '/render-ws/v1'
        inp['source_point_match_collection']['owner'] = \
            settings.RENDER_SERVICE_USER
        inp['source_point_match_collection']['match_collection'] = \
            chnk.get_point_collection_name()

        inp['first_section'] = z_start
        inp['last_section'] = z_end

        inp['solver_options']['dir_scratch'] = storage_directory

        return SolveRoughAlignmentParameters().dump(inp).data
