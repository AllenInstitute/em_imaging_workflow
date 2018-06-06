from workflow_engine.strategies import execution_strategy
from rendermodules.materialize.schemas import \
  RenderSectionAtScaleParameters
from development.models.chunk import Chunk
from workflow_engine.models.configuration import Configuration
from workflow_engine.models.well_known_file import WellKnownFile
from django.conf import settings
import simplejson as json
from development.strategies import RENDER_STACK_SOLVED
import logging


class RenderDownsampleStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.render_downsample_strategy')

    def get_input(self, em_mset, storage_directory, task):
        RenderDownsampleStrategy._log.info('get_input')

        inp = Configuration.objects.get(
            name='Render Downsample Montage Input',
            configuration_type='strategy_config').json_object

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['render']['memGB'] = '18G'

        inp['minZ'] = em_mset.section.z_index
        inp['maxZ'] = em_mset.section.z_index

        inp['input_stack'] = self.get_input_stack_name()
        inp['image_directory'] = \
            em_mset.get_storage_directory(
                settings.LONG_TERM_BASE_FILE_PATH)

        wkf = WellKnownFile.get(em_mset.reference_set, 'description')
        RenderDownsampleStrategy._log.info('WKF: %s', wkf)

        with open(wkf) as j:
            json_data = json.loads(j.read())
            inp['transform'] = json_data['transform']

        return RenderSectionAtScaleParameters().dump(inp).data

    def get_input_stack_name(self):
        return RENDER_STACK_SOLVED

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'temp_stack')

        downsample_configs = em_mset.configurations.filter(
            configuration_type='downsample temp stack')

        if len(downsample_configs) == 0:
            downsample_config = Configuration(
                content_object=em_mset,
                name='%s downsample temp_stack' % str(em_mset),
                configuration_type='downsample temp stack',
                json_object={ 
                    'downsample_temp_stack' : results['temp_stack']
                })
        else:
            downsample_config = downsample_configs.first()

        downsample_config.json_object[
            'downsample_temp_stack'] = results['temp_stack']

        if len(downsample_configs) > 1:
            RenderDownsampleStrategy.error(
                'Too many downsample stack configurations found')

        downsample_config.save()
        Chunk.assign_montage_set_to_chunks(em_mset)

