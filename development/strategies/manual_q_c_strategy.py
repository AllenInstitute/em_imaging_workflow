from workflow_engine.strategies import execution_strategy
from workflow_engine.models import *
from development.models import *
from django.conf import settings
from os import listdir

import os

class ManualQCStrategy(execution_strategy.ExecutionStrategy):

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    input_data = {}

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
