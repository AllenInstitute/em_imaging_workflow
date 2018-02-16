from workflow_engine.strategies import execution_strategy
from django.conf import settings
from development.strategies.schemas.generate_mip_maps import input_dict
from rendermodules.dataimport.schemas import GenerateMipMapsParameters
import logging
from development.strategies import RENDER_STACK_INGEST
from development.strategies.chmod_strategy import ChmodStrategy


class GenerateMipMapsStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.generate_mip_maps_strategy')
    
    def get_input(self, em_mset, storage_directory, task):
        GenerateMipMapsStrategy._log.info('get_input')

        em_mset.mipmap_directory = em_mset.get_storage_directory(
            base_storage_directory=settings.MIPMAP_FILE_PATH)
        em_mset.save()

        inp = input_dict
        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['input_stack'] = RENDER_STACK_INGEST

        inp['output_dir'] = em_mset.mipmap_directory

        inp['zstart'] = em_mset.section.z_index
        inp['zend'] = em_mset.section.z_index

        return GenerateMipMapsParameters().dump(inp).data

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'output_dir')
        em_mset.mipmap_directory =  results['output_dir']
        em_mset.save()

        ChmodStrategy.add_chmod_file(
            em_mset, results['output_dir'])
        ChmodStrategy.add_chmod_dir(
            em_mset, results['output_dir'])
        ChmodStrategy.enqueue_montage(em_mset)
