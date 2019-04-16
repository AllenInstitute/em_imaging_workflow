from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import (
    RenderStrategyUtils as RSU
)
from rendermodules.montage.schemas import SolveMontageSectionParameters
from django.conf import settings
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
import logging


class TwoDMontageSolverStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.montage.'
        'two_d_montage_solver_strategy')

    def get_input(self, em_mset, storage_directory, task):
        TwoDMontageSolverStrategy._log.info("get input")

        inp = self.get_workflow_node_input_template(task)

        inp['render'] = RSU.render_input_dict(em_mset)

        stack_names = TwoDStackNameManager.two_d_solver_stacks(em_mset)

        # TODO: verify carefully against expected
        inp['source_collection'] = RSU.collection_dict(em_mset)
        inp['source_collection']['stack'] = stack_names['source_collection']
        inp['target_collection']['stack'] = stack_names['target_collection']
        inp['source_point_match_collection'] = RSU.collection_dict(em_mset)
        inp['source_point_match_collection'][
            'match_collection'
        ] = em_mset.get_point_collection_name()

        inp['first_section'] = em_mset.section.z_index
        inp['last_section'] = em_mset.section.z_index
        inp['solver_executable'] = self.get_solver_executable_path()

        task_dir = self.get_or_create_task_storage_directory(task)
        inp['temp_dir'] = task_dir

        # this needs to match mic scratch directory
        inp['solver_options']['dir_scratch'] = em_mset.get_storage_directory()

        inp['solver_options']['Height'] = em_mset.camera.height
        inp['solver_options']['Width'] = em_mset.camera.height

        return  SolveMontageSectionParameters().dump(inp).data

    def get_solver_executable_path(self):
        return settings.MONTAGE_SOLVER_BIN

