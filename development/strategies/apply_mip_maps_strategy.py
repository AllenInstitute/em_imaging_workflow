from workflow_engine.strategies import execution_strategy
from django.conf import settings
from development.strategies.schemas.generate_mip_maps import input_dict
from rendermodules.dataimport.schemas import AddMipMapsToStackParameters
from development.strategies \
    import RENDER_STACK_INGEST, RENDER_STACK_APPLY_MIPMAPS
import logging


class ApplyMipMapsStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.apply_mip_maps_strategy')
    
    def get_input(self, em_mset, storage_directory, task):
        ApplyMipMapsStrategy._log.info('get_input')
        inp = input_dict
        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.section.specimen.uid
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['input_stack'] = RENDER_STACK_INGEST
        inp['output_stack'] = RENDER_STACK_APPLY_MIPMAPS
        inp['mipmap_dir'] = em_mset.mipmap_directory
        inp['output_dir'] = em_mset.get_storage_directory()

        inp['zstart'] = em_mset.section.z_index
        inp['zend'] = em_mset.section.z_index

        return AddMipMapsToStackParameters().dump(inp).data