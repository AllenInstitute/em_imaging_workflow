from workflow_engine.strategies import execution_strategy
from development.models import EMMontageSet
from rendermodules.pointmatch.schemas import (
    SwapPointMatches
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
from development.strategies import (
    get_workflow_node_input_template
)
from django.conf import settings
import logging


class SwapPointMatchStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'registration.swap_point_match_strategy')

    def get_input(self, reimaged_mset, storage_directory, task):
        inp = get_workflow_node_input_template(
            task,
            name='Swap Point Matches Input')

        inp['render'].update(
            TwoDStackNameManager.em_montage_set_render_settings(
                reimaged_mset
            )
        )

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

        primary_mset = em_msets[0]

        for m in em_msets:
            if ((m.id != reimaged_mset.id) and
                (m.object_state != 
                 EMMontageSet.STATE.EM_MONTAGE_SET_FAILED)):
                raise Exception(
                    'All other montage sets must be in the FAILED state'
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
