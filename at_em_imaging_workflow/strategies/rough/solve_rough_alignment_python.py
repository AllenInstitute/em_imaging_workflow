from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
from at_em_imaging_workflow.render_strategy_utils import (
    RenderStrategyUtils as RSU
)
import logging


class SolveRoughAlignmentPython(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.rough.'
        'solve_rough_alignment_python')

    def get_input(self, chnk, storage_directory, task):
        inp = self.get_workflow_node_input_template(task)

        stacks = TwoDStackNameManager.solve_rough_align_python_stacks(
            chnk,
            inp['transformation']
        )

        inp['pointmatch'] = RSU.render_input_dict(chnk)
        inp['pointmatch']['name'] = chnk.get_point_collection_name()
        inp['pointmatch']['db_interface'] = 'render'

        inp['input_stack'] = RSU.render_input_dict(chnk)
        inp['input_stack']['name'] = stacks['input_stack']
        inp['input_stack']['db_interface'] = 'render'

        inp['output_stack'] = RSU.render_input_dict(chnk)
        inp['output_stack']['name'] = stacks['output_stack']
        inp['output_stack']['db_interface'] = 'render'

        _, min_z, max_z = chnk.z_info()
        inp['first_section'] = min_z
        inp['last_section'] = max_z

        inp['close_stack'] = False

        task_dir = self.get_or_create_task_storage_directory(task)
        inp['hdf5_options']['output_dir'] = task_dir

        return EMA_Schema().dump(inp).data


try:
    from EMaligner.schemas import EMA_Schema
except:
    SolveRoughAlignmentPython._log.warning('Could not import EMA_Schema')

