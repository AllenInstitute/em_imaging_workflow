from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import (
    RenderStrategyUtils as RSU
)
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
from rendermodules.rough_align.schemas import  SolveRoughAlignmentParameters
from django.conf import settings


class SolveRoughAlignmentStrategy(InputConfigMixin, ExecutionStrategy):
    def get_input(self, chnk, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Rough Alignment Solver Input')

        _, z_start, z_end = chnk.z_info()

        inp['render'] = RSU.render_input_dict(chnk)

        stacks = TwoDStackNameManager.solve_rough_align_stacks(chnk)
        
        inp['source_collection'] = RSU.collection_dict(chnk)
        inp['source_collection']['stack'] = stacks['source']

        inp['target_collection'] = RSU.collection_dict(chnk)
        inp['target_collection']['stack'] = stacks['target']

        inp['source_point_match_collection'] = RSU.collection_dict(chnk)
        inp['source_point_match_collection'][
            'match_collection'
        ] = chnk.get_point_collection_name()

        inp['first_section'] = z_start
        inp['last_section'] = z_end

        inp['solver_options']['dir_scratch'] = storage_directory
        inp['solver_executable'] = settings.MONTAGE_SOLVER_BIN

        return SolveRoughAlignmentParameters().dump(inp).data
