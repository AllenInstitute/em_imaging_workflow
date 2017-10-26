from workflow_engine.strategies import execution_strategy
# from workflow_engine.models import *
# from development.models import *
from rendermodules.montage.schemas import \
  SolveMontageSectionParameters
from django.conf import settings
from os import listdir
import logging
import os

class TwoDMontagePointMatchStrategy(execution_strategy.ExecutionStrategy):
  _log = logging.getLogger(
    'development.strategies.two_d_montage_point_match_strategy')

  default_input = {
    "render": {
        "host": "http://em-131fs",
        "port": 8998,
        "owner": "gayathri",
        "project": "MM2",
        "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
    },
    "solver_options": {
		"min_tiles": 3,
		"degree": 1,
		"outlier_lambda": 1000,
		"solver": "backslash",
		"min_points": 4,
		"max_points": 80,
		"stvec_flag": 0,
		"conn_comp": 1,
		"distributed": 0,
		"lambda_value": 1,
		"edge_lambda": 0.1,
		"small_region_lambda": 10,
		"small_region": 5,
		"calc_confidence": 1,
		"translation_fac": 1,
		"use_peg": 1,
		"peg_weight": 0.0001,
		"peg_npoints": 5
	},
    "source_collection": {
		"stack": "mm2_acquire_8bit",
		"owner": "gayathri",
		"project": "MM2",
		"service_host": "em-131fs:8998",
		"baseURL": "http://em-131fs:8998/render-ws/v1",
		"renderbinPath": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts",
		"verbose": 0
	},
    "target_collection": {
		"stack": "mm2_acquire_8bit_Montage",
        "owner": "gayathri",
		"project": "MM2",
		"service_host": "em-131fs:8998",
		"baseURL": "http://em-131fs:8998/render-ws/v1",
		"renderbinPath": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts",
		"verbose": 0,
		"initialize": 0,
		"complete": 1
	},
    "source_point_match_collection": {
		"server": "http://em-131fs:8998/render-ws/v1",
		"owner": "gayathri_MM2",
		"match_collection": "mm2_acquire_8bit_montage"
	},
    "z_value": 1049,
	"filter_point_matches": 1,
    "solver_executable": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/EM_aligner/matlab_compiled/solve_montage_SL",
	"temp_dir": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch",
	"scratch": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch",
	"renderer_client": "/data/nc-em2/gayathrim/renderBin/bin/render.sh",
	"disableValidation": 1,
	"verbose": 0
  }

  #override if needed
  #set the data for the input file
  def get_input(self, enqueued_object, storage_directory, task):
    TwoDMontagePointMatchStrategy._log.info("get input")

    input = TwoDMontagePointMatchStrategy.default_input
    input['render']['host'] = settings.RENDER_SERVICE_URL
    input['render']['port'] = settings.RENDER_SERVICE_PORT
    input['render']['owner'] = settings.RENDER_SERVICE_USER
    input['render']['project'] = settings.RENDER_SERVICE_PROJECT

    return SolveMontageSectionParameters().dump(input).data 

  #override if needed
  #called after the execution finishes
  #process and save results to the database
  def on_finishing(self, enqueued_object, results, task):

    # self.check_key(results, 'output_json')

    # self.set_well_known_file(results['output_json'], enqueued_object, 'description', task)
    pass

  #override if needed
  #set the storage directory for an enqueued object
  #def get_storage_directory(self, base_storage_directory, job):
  #  enqueued_object = job.get_enqueued_object()
  #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
