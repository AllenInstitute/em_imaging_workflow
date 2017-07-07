from workflow_engine.strategies import manual_strategy
from development.models import *

class FavoriteNumberStrategy(manual_strategy.ManualStrategy):
  #override if needed
  #add code that returns true when a manual task is finished
  def task_finished(self, task):
    enqueued_object = task.get_enqueued_object()
    return enqueued_object.favorite_number is not None

  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, enqueued_object, results):
    pass

  #override if needed
  #this is called when a job is transitioning from a previous queue
  #given the previous job, return an array of enqueued objects for this queue
  def get_objects_for_queue(self, prev_queue_job):
    objects = []
    objects.append(prev_queue_job.get_enqueued_object())
    return objects