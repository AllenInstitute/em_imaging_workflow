from workflow_engine.strategies import ExecutionStrategy, InputConfigMixin
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
from rendermodules.rough_align.schemas import (
    ApplyRoughAlignmentTransformParameters
)
from at_em_imaging_workflow.models import EMMontageSet
import logging
import copy


class ApplyRoughAlignmentStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.rough.'
        'apply_rough_alignment_strategy')

    def get_input(self, chnk, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Apply Rough Alignment Input')

        inp['render'] = RenderStrategyUtils.render_input_dict(chnk)

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

        inp['old_z'] = [int(z) for z in mapped_from]
        inp['new_z'] = [z_mapping[z] for z in mapped_from]
        inp['map_z'] = True
        inp['consolidate_transforms'] = True
        inp['tilespec_directory'] = storage_directory

        inp.update(
            TwoDStackNameManager.apply_rough_alignment_stacks(chnk)
        )

        return ApplyRoughAlignmentTransformParameters().dump(inp).data
