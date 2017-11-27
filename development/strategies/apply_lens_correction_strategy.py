from workflow_engine.strategies import execution_strategy
from rendermodules.lens_correction.schemas import \
  ApplyLensCorrectionParameters
from development.strategies.schemas.apply_lens_correction import input_dict
from workflow_engine.models.well_known_file import WellKnownFile
from django.conf import settings
from os import listdir
import simplejson as json
import logging
import os

class ApplyLensCorrectionStrategy(execution_strategy.ExecutionStrategy):
  _log = logging.getLogger(
      'development.strategies.apply_lens_correction_strategy')

  #override if needed
  #set the data for the input file
  def get_input(self, em_mset, storage_directory, task):
    ApplyLensCorrectionStrategy._log.info('get_input')
    input = input_dict

    input['render']['host'] = settings.RENDER_SERVICE_URL
    input['render']['port'] = settings.RENDER_SERVICE_PORT
    input['render']['owner'] = settings.RENDER_SERVICE_USER
    input['render']['project'] = settings.RENDER_SERVICE_PROJECT
    input['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
    input['zs'] = [ em_mset.section.z_index ]
    input['inputStack'] = self.get_input_stack_name()
    input['outputStack'] = self.get_input_stack_name()
    input['close_stack'] = self.get_input_stack_name()

    wkf = WellKnownFile.get(em_mset.reference_set, 'description')
    ApplyLensCorrectionStrategy._log.info('WKF: %s' % (wkf))

    with open(wkf) as j:
        json_data = json.loads(j.read())
        input['transform'] = json_data['transform']

    return ApplyLensCorrectionParameters().dump(input).data

  def get_input_stack_name(self):
    return settings.RENDER_STACK_NAME

  def get_output_stack_name(self):
    return settings.RENDER_STACK_NAME


  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, em_mset, results, task):
    # self.check_key(results, 'output_json')
    # self.set_well_known_file(results['output_json'], enqueued_object, 'description', task)
    pass

  #override if needed
  #set the storage directory for an enqueued object
  #def get_storage_directory(self, base_storage_directory, job):
  #  enqueued_object = job.get_enqueued_object()
  #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
