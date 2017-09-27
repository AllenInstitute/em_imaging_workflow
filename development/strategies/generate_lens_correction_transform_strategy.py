from workflow_engine.strategies import execution_strategy
from workflow_engine.models import *
from development.models import *
from django.conf import settings
from os import listdir

import os

class GenerateLensCorrectionTransformStrategy(execution_strategy.ExecutionStrategy):

  def find_manifest_path(self, project_path):
    manifest_path = None

    for file_name in listdir(project_path):
      full_name = os.path.join(project_path, file_name)
      if os.path.isfile(full_name) and '_trackem_' in full_name:
        if manifest_path is not None:
          raise Exception('Found multiple manifest_path files (' + str(manifest_path) + ' and ' + str(full_name) + ' ) in the ' + str(project_path) + ' directory') 
        else:
          manifest_path = full_name

    if manifest_path is None:
      raise Exception('Could not find a manifest_path in the ' + str(project_path) + ' directory')

    return manifest_path

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    '''
    Args:
        enqueued_object (ReferenceSet) assuming this based on project_path
    '''
    input_data = {}

    project_path = enqueued_object.project_path

    input_data['manifest_path'] = self.find_manifest_path(project_path)
    input_data['project_path'] = project_path

    input_data['fiji_path'] = settings.FIJI_PATH
    input_data['grid_size'] = settings.GRID_SIZE
    input_data['heap_size'] = settings.HEAP_SIZE
    input_data['outfile'] = os.path.join(storage_directory, 'test_LC.json')
    input_data['processing_directory'] = storage_directory

    sift_params = {}
    sift_params['initialSigma'] = settings.INITIAL_SIGMA
    sift_params['steps'] = settings.STEPS
    sift_params['minOctaveSize'] = settings.MIN_OCTAVE_SIZE
    sift_params['maxOctaveSize'] = settings.MAX_OCTAVE_SIZE
    sift_params['fdSize'] = settings.FD_SIZE
    sift_params['fdBins'] = settings.FD_BINS

    input_data['SIFT_params'] = sift_params

    align_params = {}
    align_params['rod'] = settings.ROD
    align_params['maxEpsilon'] = settings.MAX_EPSILON
    align_params['minInlierRatio'] = settings.MIN_INLIER_RATIO
    align_params['minNumInliers'] = settings.MIN_NUMBER_INLIERS
    align_params['expectedModelIndex'] = settings.EXPECTED_MODEL_INDEX
    align_params['multipleHypotheses'] = settings.MULTIPLE_HYPOTHESES
    align_params['rejectIdentity'] = settings.REJECT_IDENTITY
    align_params['identityTolerance'] = settings.IDENTITY_TOLERANCE
    align_params['tilesAreInPlace'] = settings.TILES_ARE_IN_PLACE
    align_params['desiredModelIndex'] = settings.DESIRED_MODEL_INDEX
    align_params['regularize'] = settings.REGULARIZE
    align_params['maxIterationsOptimize'] = settings.MAX_ITERATIONS_OPTIMIZE
    align_params['maxPlateauWidthOptimize'] = settings.MAX_PLATEAU_WIDTH_OPTIMIZE
    align_params['dimension'] = settings.DIMENSION
    align_params['lambdaVal'] = settings.LAMBDA_VAL
    align_params['clearTransform'] = settings.CLEAR_TRANSFORM
    align_params['visualize'] = settings.VISUALIZE

    input_data['align_params'] = align_params

    return input_data

  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, enqueued_object, results, task):

    self.check_key(results, 'output_json')

    self.set_well_known_file(results['output_json'], enqueued_object, 'description', task)

  #override if needed
  #set the storage directory for an enqueued object
  def get_storage_directory(self, base_storage_directory, job):
    enqueued_object = job.get_enqueued_object()
    return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
