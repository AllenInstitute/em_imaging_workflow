from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import (
    RenderStrategyUtils as RSU
)
from rendermodules.rough_align.schemas import (
    SolveRoughAlignmentParameters
)
import copy
from at_em_imaging_workflow.models import EMMontageSet
from at_em_imaging_workflow.strategies import (
    RENDER_STACK_DOWNSAMPLED,
    RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE
)
from django.conf import settings


class SolveRoughAlignmentStrategy(InputConfigMixin, ExecutionStrategy):

    # deprecate for chunk.get_load
    @classmethod
    def get_load(cls, chnk):
        chunk_section = chnk.sections.first()
        load_mset = EMMontageSet.objects.filter(
            section=chunk_section).last()

        return load_mset.sample_holder.load

    # deprecate for load.get_z_mapping
    @classmethod
    def get_z_mapping(cls, load):
        return copy.deepcopy(
            load.configurations.get(
                configuration_type='z_mapping').json_object)

    @classmethod
    def calculate_z_min_max(cls, tile_pair_ranges):
        min_z = min([rng['minz'] for rng in tile_pair_ranges.values()])
        max_z = max([rng['maxz'] for rng in tile_pair_ranges.values()])

        return min_z,max_z

    @classmethod
    def clip_z_mapping_to_min_max(cls, z_mapping, min_z, max_z):
        clipped_mapping = {
            k: v for k,v in z_mapping.items() if v >= min_z and v <= max_z
        }

        return clipped_mapping

    def get_input(self, chnk, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Rough Alignment Solver Input')

        # TODO: consolidate
        z_mapping = chnk.get_z_mapping()
        tile_pair_ranges = chnk.get_tile_pair_ranges()
        min_z, max_z = \
            SolveRoughAlignmentStrategy.calculate_z_min_max(tile_pair_ranges)
        clipped_z_mapping = \
            SolveRoughAlignmentStrategy.clip_z_mapping_to_min_max(
                z_mapping, min_z, max_z)

        zs = [int(z) for z in clipped_z_mapping.values()]
        z_start = min(zs)
        z_end = max(zs)

        inp['render'] = RSU.render_input_dict(chnk)

        inp['source_collection'] = RSU.collection_dict(chnk)
        inp['source_collection']['stack'] = RENDER_STACK_DOWNSAMPLED

        inp['target_collection'] = RSU.collection_dict(chnk)
        inp['target_collection'][
            'stack'
        ] = RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE % (z_start, z_end)

        inp['source_point_match_collection'] =RSU.collection_dict(chnk)
        inp['source_point_match_collection'][
            'match_collection'
        ] = chnk.get_point_collection_name()

        inp['first_section'] = z_start
        inp['last_section'] = z_end

        inp['solver_options']['dir_scratch'] = storage_directory
        inp['solver_executable'] = settings.MONTAGE_SOLVER_BIN

        return SolveRoughAlignmentParameters().dump(inp).data
