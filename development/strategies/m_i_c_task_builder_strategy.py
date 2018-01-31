from workflow_engine.strategies import execution_strategy
from development.strategies.schemas.m_i_c_task_builder import input_dict
from rendermodules.intensity_correction.schemas import \
    MakeMedianParams 
from django.conf import settings
import logging
import copy


class MICTaskBuilderStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger('development.strategies.m_i_c_task_builder_strategy')

    def get_input(self, em_mset, storage_directory, task):
        '''
        Args:
            em_mset (EMMontageSet) the enqueued object
        '''
        MICTaskBuilderStrategy._log.info('MIC Task Builder')
        inp = copy.deepcopy(input_dict)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['render']['output_dir'] = em_mset.storage_directory
        inp['input_stack'] = em_mset.render_stack_name()
        inp['output_stack'] = em_mset.render_stack_name()
        inp['minZ'] = em_mset.section.z_index
        inp['maxZ'] = em_mset.section.z_index

        return MakeMedianParams().dump(inp).data

