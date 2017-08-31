from workflow_engine.strategies import execution_strategy
from workflow_engine.models import *
from development.models import *

import os

class ApplyToPreviouslyUploadedMontageSetsStrategy(execution_strategy.ExecutionStrategy):

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    input_data = {}
    input_data['input'] = str(enqueued_object)
    return input_data

  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, enqueued_object, results, task):
    pass

  #override if needed
  #this is called when a job is transitioning from a previous queue
  #given the previous job, return an array of enqueued objects for this queue
  #def get_objects_for_queue(self, prev_queue_job):
  #  objects = []
  #  objects.append(prev_queue_job.get_enqueued_object())
  #  return objects

  #override if needed
  #return one or more task enqueued objects for a job enqueued object
  #def get_task_objects_for_queue(self, enqueued_object):
  #  objects = []
  #  objects.append(enqueued_object)
  #  return objects

  #override if needed
  #set the storage directory for an enqueued object
  #def get_storage_directory(self, base_storage_directory, job):
  #  enqueued_object = job.get_enqueued_object()
  #  return os.path.join(base_storage_directory, str(enqueued_object.id))

  #override if needed
  #called before the job starts running
  #def prep_job(self, job):
  #    pass

  #override if needed
  #called before the task starts running
  #def prep_task(self, task):
  #    pass

  #override if needed
  #called if the task fails
  #def on_failure(self, task):
  #  pass

  #override if needed
  #called when the task starts running
  #def on_running(self, task):
  #  pass

  #override if needed
  #def can_transition(self, enqueued_object):
  #  return True
  #override if needed
  #def skip_execution(self, enqueued_object):
  #  return False
