from workflow_engine.strategies import execution_strategy
from django.conf import settings
from development.strategies.schemas.generate_mip_maps import input_dict
from rendermodules.dataimport.schemas import GenerateMipMapsParameters
import logging


class GenerateMipMapsStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.generate_mip_maps_strategy')
    
    def get_input(self, em_mset, storage_directory, task):
        GenerateMipMapsStrategy._log.info('get_input')

        em_mset.mipmap_directory = \
            self.get_or_create_task_storage_directory(task)
        em_mset.save()

        inp = input_dict
        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['input_stack'] = em_mset.render_stack_name()

        inp['output_dir'] = em_mset.mipmap_directory

        inp['zstart'] = em_mset.section.z_index
        inp['zend'] = em_mset.section.z_index

        return GenerateMipMapsParameters().dump(inp).data

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'output_dir')
        em_mset.mipmap_directory =  results['output_dir']
        em_mset.save()
