from workflow_engine.strategies import execution_strategy
from rendermodules.stack.schemas import (
    SwapZsParameters
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
from at_em_imaging_workflow.strategies import (
    get_workflow_node_input_template
)
from at_em_imaging_workflow.models import (
    EMMontageSet
)
import logging


class SwapZsStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'registration.swap_zs_strategy')

    def get_input(self, reimaged_mset, storage_directory, task):
        cfg,created = reimaged_mset.configurations.get_or_create(
            configuration_type='rough_align_parameters',
            defaults= {
                'name': 'rough align params for montage set {}'.format(
                    reimaged_mset.id),
                'json_object': { 'reimage_index': 0 }
            })

        if created is False:
            raise Exception(
                'Montage set may have already been swapped'
            )

        inp = get_workflow_node_input_template(
            task,
            name='Swap Zs Input')

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

        # TODO: use exclude here to filter the passed one.
        em_msets = [
            m.emmontageset 
            for m
            in reimaged_mset.section.montageset_set.order_by('id')
        ]

        primary_mset = em_msets[0].emmontageset

        cfg2,created2 = primary_mset.configurations.get_or_create(
            configuration_type='rough_align_parameters',
            defaults= {
                'name': 'rough align params for montage set {}'.format(
                    primary_mset.id),
                'json_object': { 'reimage_index': 1 }
            })

        if created2 is False:
            raise Exception(
                'Montage set may have already been swapped'
            )

        for m in em_msets:
            if ((m.id != reimaged_mset.id) and
                (not (m.object_state in [
                    EMMontageSet.STATE.EM_MONTAGE_SET_FAILED,
                    EMMontageSet.STATE.EM_MONTAGE_SET_QC_FAILED,
                    EMMontageSet.STATE.EM_MONTAGE_SET_NOT_SELECTED]))):
                raise Exception(
                    'All other montage sets must be in the FAILED, MONTAGE_QC_FAILED or REIMAGE_NOT_SELECTED state'
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
            TwoDStackNameManager.swap_zs_stacks(
                primary_mset,
                reimaged_mset
            )
        )

        z = primary_mset.section.z_index

        inp['zValues'] = [
            [z], # ingest/raw
            [z], # lens corrected
            [z], # mipmaps
            [z] # solved python
        ]

        return SwapZsParameters().dump(inp).data
