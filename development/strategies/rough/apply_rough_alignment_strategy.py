from workflow_engine.strategies import execution_strategy
from rendermodules.rough_align.schemas \
    import ApplyRoughAlignmentTransformParameters
from development.strategies import RENDER_STACK_SOLVED_PYTHON, \
    RENDER_STACK_ROUGH_ALIGN, RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE, \
    get_workflow_node_input_template
from development.models import EMMontageSet
from django.conf import settings
import logging
import copy


class ApplyRoughAlignmentStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.apply_rough_alignment_strategy')

    def get_input(self, chnk, storage_directory, task):
        inp = get_workflow_node_input_template(
            task,
            name='Apply Rough Alignment Input')

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        z_mapping = copy.deepcopy(chnk.get_z_mapping())

        em_msets = EMMontageSet.objects.filter(
            section__z_index__in=z_mapping
        )

        for em_mset in em_msets:
            if (em_mset.object_state in [
                EMMontageSet.STATE.EM_MONTAGE_SET_FAILED,
                EMMontageSet.STATE.EM_MONTAGE_SET_GAP,
                EMMontageSet.STATE.EM_MONTAGE_SET_REPAIR
                ]) and (
                    em_mset.reimage_index() == 0
                ):
                del z_mapping[str(em_mset.section.z_index)] 

        mapped_from = z_mapping.keys()

        old_zs = [int(z) for z in mapped_from]
        new_zs = [z_mapping[z] for z in mapped_from]
        inp['map_z'] = True

        inp['consolidate_transforms'] = True
        inp['old_z'] = old_zs
        inp['new_z'] = new_zs
        z_start = min(new_zs)
        z_end = max(new_zs)

        inp['tilespec_directory'] = storage_directory

        inp['montage_stack'] = RENDER_STACK_SOLVED_PYTHON
        inp['prealigned_stack'] = RENDER_STACK_SOLVED_PYTHON # RENDER_STACK_LENS_CORRECTED
        inp['lowres_stack'] = RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE % (
            z_start, z_end)
        #inp['lowres_stack'] = 'rough_aligned_downsample_0_01_affine_z_mapped'
        inp['output_stack'] = RENDER_STACK_ROUGH_ALIGN % (
            z_start, z_end)

        return ApplyRoughAlignmentTransformParameters().dump(inp).data
