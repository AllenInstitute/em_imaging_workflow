from workflow_engine.strategies.execution_strategy \
    import ExecutionStrategy
import copy
from workflow_engine.models.configuration import Configuration
from development.strategies \
    import RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE, RENDER_STACK_ROUGH_SOLVED
from django.conf import settings
import logging


class SolveRoughAlignmentPython(ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.rough.solve_rough_alignment_python')

    def get_input(self, chnk, storage_directory, task):
        inp = Configuration.objects.get(
            name='Rough Align Python Solver Input',
            configuration_type='strategy_config').json_object

        z_cfg = copy.deepcopy(chnk.configurations.get(
            configuration_type='z_mapping').json_object)
        del z_cfg['tile_pair_ranges']

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
        inp['input_stack']['name'] = \
            RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE.format(z_start, z_end)
        inp['input_stack']['db_interface'] = 'render'

        inp['output_stack']['host'] = settings.RENDER_SERVICE_URL
        inp['output_stack']['port'] = settings.RENDER_SERVICE_PORT
        inp['output_stack']['owner'] = settings.RENDER_SERVICE_USER
        inp['output_stack']['project'] = chnk.get_render_project_name()
        inp['output_stack']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['output_stack']['name'] = RENDER_STACK_ROUGH_SOLVED
        inp['output_stack']['db_interface'] = 'render'

        zs = [int(z) for z in z_cfg.keys()]
        z_start = min(zs)
        z_end = max(zs)
        inp['first_section'] = z_start
        inp['last_section'] = z_end

        inp['solve_type'] = 'rough_align'
        inp['close_stack'] = False

        task_dir = self.get_or_create_task_storage_directory(task)
        inp['hdf5_options']['output_dir'] = task_dir

        return EMA_Schema().dump(inp).data


try:
    from EMaligner.EM_aligner_python_schema import EMA_Schema
except:
    SolveRoughAlignmentPython._log.warn('Could not import EMA_Schema')

