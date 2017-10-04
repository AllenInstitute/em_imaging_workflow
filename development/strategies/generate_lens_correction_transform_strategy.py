from workflow_engine.strategies import execution_strategy
from workflow_engine.models import *
from development.models import *
from rendermodules.lens_correction.schemas import \
    LensCorrectionParameters, SIFTParameters, AlignmentParameters

from django.conf import settings
from os import listdir
import os


class GenerateLensCorrectionTransformStrategy(execution_strategy.ExecutionStrategy):
  default_input = {
      "manifest_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/lc_test_data/Wij_Set_594451332/594089217_594451332/_trackem_20170502174048_295434_5LC_0064_01_20170502174047_reference_0_.txt",
      "project_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/lc_test_data/Wij_Set_594451332/594089217_594451332/",
      "fiji_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/Fiji.app/ImageJ-linux64",
      "grid_size": 3,
      "heap_size": 20,
      "outfile": "test_LC.json",
      "processing_directory": None,
      "SIFT_params": {
          "initialSigma": 1.6,
          "steps": 3,
          "minOctaveSize": 800,
          "maxOctaveSize": 1200,
          "fdSize": 4,
          "fdBins": 8
      },
      "align_params": {
          "rod": 0.92,
          "maxEpsilon": 5.0,
          "minInlierRatio": 0.0,
          "minNumInliers": 5,
          "expectedModelIndex": 1,
          "multipleHypotheses": True,
          "rejectIdentity": True,
          "identityTolerance": 5.0,
          "tilesAreInPlace": True,
          "desiredModelIndex": 0,
          "regularize": False,
          "maxIterationsOptimize": 2000,
          "maxPlateauWidthOptimize": 200,
          "dimension": 5,
          "lambdaVal": 0.01,
          "clearTransform": True,
          "visualize": False
      }}

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
    project_path = enqueued_object.project_path
    
    input = GenerateLensCorrectionTransformStrategy.default_input
    
    input['manifest_path'] = self.find_manifest_path(project_path)
    input['project_path'] = project_path
    input['outfile'] = os.path.join(storage_directory, 'test_LC.json')
    input['processing_directory'] = storage_directory
    
    return LensCorrectionParameters().dump(input).data
    

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
