from workflow_engine.strategies.execution_strategy import (
    ExecutionStrategy
)
from development.strategies import (
    RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE,
    RENDER_STACK_RIGID_ALIGN_DOWNSAMPLE,
    RENDER_STACK_DOWNSAMPLED,
    get_workflow_node_input_template
)
from development.strategies.rough.solve_rough_alignment_strategy import ()
    SolveRoughAlignmentStrategy as SRAS
)
from django.conf import settings
import logging


class SolveRoughAlignmentPython(ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.rough.solve_rough_alignment_python')

    def get_input(self, chnk, storage_directory, task):
        inp = get_workflow_node_input_template(task)

        tile_pair_ranges = \
            SRAS.get_tile_pair_ranges(chnk)
        min_z, max_z = \
            SRAS.calculate_z_min_max(tile_pair_ranges)

        input_stack_template = RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE
        output_stack_template = None

        if inp['transformation'] == 'rigid':
            input_stack = RENDER_STACK_DOWNSAMPLED
            output_stack = RENDER_STACK_RIGID_ALIGN_DOWNSAMPLE % (min_z, max_z)
        elif inp['transformation'] == 'affine':
            input_stack = RENDER_STACK_RIGID_ALIGN_DOWNSAMPLE % (min_z, max_z)
            output_stack = RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE % (min_z, max_z)
        else:
            raise Exception(
                'transformation must be rigid or affine')

        inp['pointmatch']['host'] = settings.RENDER_SERVICE_URL
        inp['pointmatch']['port'] = settings.RENDER_SERVICE_PORT
        inp['pointmatch']['owner'] = settings.RENDER_SERVICE_USER
        inp['pointmatch']['project'] = chnk.get_render_project_name()
        inp['pointmatch']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['pointmatch']['name'] = chnk.get_point_collection_name()
        inp['pointmatch']['db_interface'] = 'render'

        inp['input_stack']['host'] = settings.RENDER_SERVICE_URL
        inp['input_stack']['port'] = settings.RENDER_SERVICE_PORT
        inp['input_stack']['owner'] = settings.RENDER_SERVICE_USER
        inp['input_stack']['project'] = chnk.get_render_project_name()
        inp['input_stack']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['input_stack']['name'] = input_stack
        inp['input_stack']['db_interface'] = 'render'

        inp['output_stack']['host'] = settings.RENDER_SERVICE_URL
        inp['output_stack']['port'] = settings.RENDER_SERVICE_PORT
        inp['output_stack']['owner'] = settings.RENDER_SERVICE_USER
        inp['output_stack']['project'] = chnk.get_render_project_name()
        inp['output_stack']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['output_stack']['name'] = output_stack
        inp['output_stack']['db_interface'] = 'render'

        inp['first_section'] = min_z
        inp['last_section'] = max_z

        inp['close_stack'] = False

        task_dir = self.get_or_create_task_storage_directory(task)
        inp['hdf5_options']['output_dir'] = task_dir

        return EMA_Schema().dump(inp).data


try:
    from EMaligner.schemas import EMA_Schema
except:
    SolveRoughAlignmentPython._log.warn('Could not import EMA_Schema')

