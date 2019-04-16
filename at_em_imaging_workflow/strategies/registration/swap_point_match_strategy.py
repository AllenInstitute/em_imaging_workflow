from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
from at_em_imaging_workflow.models import EMMontageSet
from rendermodules.pointmatch.schemas import SwapPointMatches
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
from django.conf import settings
import logging


class SwapPointMatchStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'registration.swap_point_match_strategy')

    def get_input(self, reimaged_mset, storage_directory, task):
        try:
            cfg = reimaged_mset.configurations.get(
                configuration_type='rough_align_parameters',
            )
            cfg_json = cfg.json_object
        except:
            raise Exception(
                'Montage set does not appear to have been through Swap Z'
            )

        if 'swap_point_match_index' in cfg_json:
            raise Exception(
                'Cannot run Swap Point Match twice'
            )
        else:
            cfg_json['swap_point_match_index'] = 0
            cfg.save()

        inp = self.get_workflow_node_input_template(
            task,
            name='Swap Point Matches Input')

        inp['render'] = RenderStrategyUtils.render_input_dict(
            reimaged_mset)

        if (reimaged_mset.object_state != 
            EMMontageSet.STATE.EM_MONTAGE_SET_QC_PASSED):
            raise Exception(
                'Montage set to be swapped out must be in QC passed state'
            )

        em_msets = [
            m.emmontageset 
            for m
            in reimaged_mset.section.montageset_set.order_by('id')
        ]

        primary_mset = em_msets[0].emmontageset

        try:
            cfg2 = primary_mset.configurations.get(
                configuration_type='rough_align_parameters',
            )
            cfg2_json = cfg2.json_object
        except:
            raise Exception(
                'Montage set does not appear to have been through Swap Z'
            )

        if 'swap_point_match_index' in cfg2_json:
            raise Exception(
                'Cannot run Swap Point Match twice'
            )
        else:
            cfg2_json['swap_point_match_index'] = 1
            cfg2.save()

        for m in em_msets:
            if ((m.id != reimaged_mset.id) and
                (not (m.object_state in [
                    EMMontageSet.STATE.EM_MONTAGE_SET_FAILED,
                    EMMontageSet.STATE.EM_MONTAGE_SET_QC_FAILED,
                    EMMontageSet.STATE.EM_MONTAGE_SET_NOT_SELECTED]))):
                raise Exception(
                    'All other montage sets must be in the FAILED, MONTAGE_QC_FAILED, or REIMAGED_NOT_SELECTED state'
                )

        if not (reimaged_mset in em_msets):
            raise Exception(
                'Swapped montage sets must have the same section.'
            )

        if reimaged_mset.reimage_index() == 0:
            raise Exception(
                'Enqueued object is already the primary montage set.'
            )

        if (reimaged_mset.id == primary_mset.id):
            raise Exception(
                'Primary and reimage montage set are identical'
            )

        inp.update(
            TwoDStackNameManager.swap_point_match_collections(
                primary_mset,
                reimaged_mset
            )
        )

        inp['zValues'] = [
            primary_mset.section.z_index
        ]
        inp['match_owner'] = settings.RENDER_SERVICE_USER

        return SwapPointMatches().dump(inp).data
