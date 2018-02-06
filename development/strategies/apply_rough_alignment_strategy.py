from workflow_engine.strategies import execution_strategy
from rendermodules.rough_align.schemas \
    import ApplyRoughAlignmentTransformParameters
from development.strategies.schemas.apply_rough_alignment import input_dict
from development.strategies import RENDER_STACK_SOLVED,\
    RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE, RENDER_STACK_ROUGH_ALIGN,\
    RENDER_STACK_LENS_CORRECTED
from development.models.chunk import Chunk
from django.conf import settings
import copy


class ApplyRoughAlignmentStrategy(execution_strategy.ExecutionStrategy):

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

        inp['tilespec_directory'] = storage_directory

        inp['montage_stack'] = RENDER_STACK_SOLVED
        inp['prealigned_stack'] = RENDER_STACK_LENS_CORRECTED
        inp['lowres_stack'] = RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE % (
            z_start, z_end)
        inp['output_stack'] = RENDER_STACK_ROUGH_ALIGN % (
            z_start, z_end)

        return ApplyRoughAlignmentTransformParameters().dump(inp).data
