from workflow_engine.strategies import execution_strategy
from rendermodules.materialize.schemas import \
  RenderSectionAtScaleParameters
from development.strategies.schemas.render_downsample import input_dict
from workflow_engine.models.well_known_file import WellKnownFile
from django.conf import settings
import simplejson as json
import logging

class RenderDownsampleStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.render_downsample_strategy')
    
    #override if needed
    #set the data for the input file
    def get_input(self, em_mset, storage_directory, task):
        RenderDownsampleStrategy._log.info('get_input')
        inp = input_dict

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['minZ'] = em_mset.section.z_index
        inp['maxZ'] = em_mset.section.z_index
        inp['input_stack'] = self.get_input_stack_name()
        inp['image_directory'] = self.get_or_create_task_storage_directory(task)

        wkf = WellKnownFile.get(em_mset.reference_set, 'description')
        RenderDownsampleStrategy._log.info('WKF: %s', wkf)

        with open(wkf) as j:
            json_data = json.loads(j.read())
            inp['transform'] = json_data['transform']

        return RenderSectionAtScaleParameters().dump(inp).data

    def get_input_stack_name(self):
        return settings.RENDER_STACK_NAME
