from workflow_engine.strategies import execution_strategy
from rendermodules.lens_correction.schemas import \
  ApplyLensCorrectionParameters
from development.strategies.schemas.apply_lens_correction import input_dict
from workflow_engine.models.well_known_file import WellKnownFile
from django.conf import settings
import simplejson as json
import logging
from development.strategies \
    import RENDER_STACK_APPLY_MIPMAPS, RENDER_STACK_LENS_CORRECTED

class ApplyLensCorrectionStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.apply_lens_correction_strategy')
    
    #override if needed
    #set the data for the input file
    def get_input(self, em_mset, storage_directory, task):
        ApplyLensCorrectionStrategy._log.info('get_input')
        inp = input_dict

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['zs'] = [ em_mset.section.z_index ]
        inp['inputStack'] = RENDER_STACK_APPLY_MIPMAPS
        inp['outputStack'] = RENDER_STACK_LENS_CORRECTED
        inp['close_stack'] = False

        wkf = WellKnownFile.get(em_mset.reference_set, 'description')
        ApplyLensCorrectionStrategy._log.info('WKF: %s' % (wkf))

        with open(wkf) as j:
            json_data = json.loads(j.read())
            inp['transform'] = json_data['transform']

        return ApplyLensCorrectionParameters().dump(inp).data

