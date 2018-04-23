from workflow_engine.strategies import execution_strategy
from rendermodules.dataimport.schemas \
    import MakeMontageScapeSectionStackParameters
from development.strategies.schemas.rough.make_montage_scapes_stack \
     import input_dict
from development.strategies import RENDER_STACK_SOLVED, \
    RENDER_STACK_ROUGH_ALIGN_SCAPES_STACK
from django.conf import settings
import copy


class MakeMontageScapesStackStrategy(execution_strategy.ExecutionStrategy):

    def get_input(self, chnk, storage_directory, task):
        inp = copy.deepcopy(input_dict)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        (z_start, z_end) = chnk.z_range()
        inp['minZ'] = z_start
        inp['maxZ'] = z_end

        inp['image_directory'] = storage_directory

        inp['montage_stack'] = RENDER_STACK_SOLVED
        inp['output_stack'] = RENDER_STACK_ROUGH_ALIGN_SCAPES_STACK % (
            z_start, z_end)

        return MakeMontageScapeSectionStackParameters().dump(inp).data
