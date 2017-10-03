from workflow_engine.strategies import execution_strategy
from workflow_engine.models import *
from development.models import *
from django.conf import settings
from os import listdir
import jinja2
import simplejson as json
import os

class GeneratePointMatchesStrategy(execution_strategy.ExecutionStrategy):
  def get_template(self): 
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('development.strategies',
                                    'templates'))
    return env.get_template('generate_point_matches_template.json')

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    input_data_template = self.get_template()

    # port = enqueued_object.service.port
    port = 8998

    return json.loads(
        input_data_template.render(
            render_service_port=port))

    return input_data

  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, enqueued_object, results, task):

    self.check_key(results, 'output_json')

    self.set_well_known_file(results['output_json'], enqueued_object, 'description', task)

  #override if needed
  #set the storage directory for an enqueued object
  #def get_storage_directory(self, base_storage_directory, job):
  #  enqueued_object = job.get_enqueued_object()
  #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
