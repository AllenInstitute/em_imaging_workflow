from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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

        try:
            z_mapping = chnk.configurations.get(
                configuration_type='z_mapping').json_object
            old_zs = chnk.z_list()
            mapped_from = json_object.keys()

            if set(old_zs) != set(mapped_from):
                raise Exception("Z mapping doesn't match chunk sections")

            new_zs = [mapped_from[z] for z in mapped_from]
        except ObjectDoesNotExist as e:
            ApplyRoughAlignmentStrategy._log.warning('No Z Mapping, using 1-1')
            old_zs = chnk.z_list()
            new_zs = old_zs
        except MultipleObjectsReturned as e:
            ApplyRoughAlignmentStrategy._log.error("Multiple Z Mappings found")
            raise e

        # TODO: use old z and new z
        # see apply_rough_alignment_to_montages.
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
