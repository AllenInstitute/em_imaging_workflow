from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import copy
from workflow_engine.strategies import execution_strategy
from rendermodules.rough_align.schemas \
    import ApplyRoughAlignmentTransformParameters
from workflow_engine.models.configuration import Configuration
from development.strategies import RENDER_STACK_SOLVED,\
    RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE, RENDER_STACK_ROUGH_ALIGN,\
    RENDER_STACK_LENS_CORRECTED
from django.conf import settings
import logging


class ApplyRoughAlignmentStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.apply_rough_alignment_strategy')

    def get_input(self, chnk, storage_directory, task):
        inp = Configuration.objects.get(
            name='Apply Rough Alignment Input',
            configuration_type='strategy_config').json_object

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        z_mapping = copy.deepcopy(chnk.configurations.get(
            configuration_type='z_mapping').json_object)
        del z_mapping['tile_pair_ranges']
        # old_zs = chnk.z_list()
        mapped_from = z_mapping.keys()

        old_zs = [int(z) for z in mapped_from]
        new_zs = [z_mapping[z] for z in mapped_from]
        inp['map_z'] = True
        inp['consolidate_transforms'] = True
        inp['old_z'] = old_zs
        inp['new_z'] = new_zs
        z_start = min(old_zs)
        z_end = max(old_zs)

        inp['tilespec_directory'] = storage_directory

        inp['montage_stack'] = RENDER_STACK_SOLVED
        inp['prealigned_stack'] = RENDER_STACK_SOLVED # RENDER_STACK_LENS_CORRECTED
        #inp['lowres_stack'] = RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE % (
        #    z_start, z_end)
        inp['lowres_stack'] = 'rough_aligned_downsample_0_01_affine_z_mapped'
        inp['output_stack'] = RENDER_STACK_ROUGH_ALIGN % (
            z_start, z_end)

        return ApplyRoughAlignmentTransformParameters().dump(inp).data
