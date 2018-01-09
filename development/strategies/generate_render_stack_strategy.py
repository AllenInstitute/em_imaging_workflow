from workflow_engine.strategies import execution_strategy
from development.strategies.schemas.generate_render_stack import input_dict
from rendermodules.dataimport.schemas import \
    GenerateEMTileSpecsParameters
from development.models.e_m_montage_set import EMMontageSet
from development.strategies import RENDER_STACK_INGEST
from django.conf import settings
import copy
import logging


class GenerateRenderStackStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.ingest_generate_render_stack_strategy')

    #override if needed
    #set the data for the input file
    def get_input(self, em_set, storage_directory, task):
        '''
        Args:
            em_set (EMMontageSet) the enqueued object
        '''
        GenerateRenderStackStrategy._log.info(
            'ingest/generate render stack')
        inp = copy.deepcopy(input_dict)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['stack'] = RENDER_STACK_INGEST
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['metafile'] = em_set.metafile
        inp['close_stack'] = False
        inp['z_index'] = self.get_z_index(em_set)

        return GenerateEMTileSpecsParameters().dump(inp).data

    def get_z_index(self, em_set):
        return em_set.section.z_index

    def can_transition(self, enqueued_object):
        is_em_montage_set = isinstance(enqueued_object, EMMontageSet)

        return is_em_montage_set
