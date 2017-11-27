from workflow_engine.strategies.execution_strategy import ExecutionStrategy
from rendermodules.lens_correction.schemas \
    import LensCorrectionParameters
from development.strategies.schemas.generate_lens_correction_transform import input_dict
from django.conf import settings
from os import listdir
import logging
import os


class GenerateLensCorrectionTransformStrategy(ExecutionStrategy):
  _log = logging.getLogger('development.strategies.generate_lens_correction_transform_strategy')

  # def skip_execution(self, enqueued_object):
  #    return True

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    '''
    Args:
        enqueued_object (ReferenceSet)
    '''
    project_path = enqueued_object.storage_directory
    GenerateLensCorrectionTransformStrategy._log.info(
        'project path: %s' % (project_path))
    
    input = input_dict 
    
    input['manifest_path'] = enqueued_object.manifest_path
    input['project_path'] = project_path
    input['fiji_path'] = settings.FIJI_PATH
    input['outfile'] = os.path.join(storage_directory,
                                    'lens_correction_out.json')
    input['processing_directory'] = storage_directory
    
    return LensCorrectionParameters().dump(input).data
    

  def on_finishing(self, enqueued_object, results, task):
    ''' called after the execution finishes
        process and save results to the database
    '''
    self.check_key(results, 'output_json')

    GenerateLensCorrectionTransformStrategy._log.info(
        'lens_correction_transform output %s' % (str(results)))
    self.set_well_known_file(
        results['output_json'],
        enqueued_object,
        'description',
        task)

  #override if needed
  #set the storage directory for an enqueued object
  def get_storage_directory(self, base_storage_directory, job):
    enqueued_object = job.get_enqueued_object()
    return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
