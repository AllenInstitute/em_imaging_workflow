import pytest
import simplejson as json


@pytest.fixture
def mock_run_states():
    rs = {}
    for s in [
        'PENDING',
        'QUEUED',
        'RUNNING',
        'FINISHED_EXECUTION',
        'FAILED_EXECUTION',
        'SUCCESS',
        'FAILED']:
        rs[s], _ = RunState.objects.update_or_create(
            name=s)
    return rs


@pytest.fixture
def strategy_configurations():
    strategy_configurations.configs = """{
 "Render Downsample Montage Input": {
  "scale": 0.01,
  "render": {
    "host": "http://em-131fs",
    "port": 8080,
    "owner": "russelt",
    "project": "Reflections",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
  },
  "zValues": [
    1047
  ],
  "imgformat": "png",
  "input_stack": "Secs_1015_1099_5_reflections_mml6_montage",
  "image_directory": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/scratch"
},
        "Detect Montage Defects Input": {
  "maxZ": 1029,
  "minZ": 1028,
  "render": {
    "host": "http://em-131fs",
    "port": 8080,
    "owner": "danielk",
    "project": "Seams",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_latest/render-ws-java-client/src/main/scripts"
  },
  "pool_size": 20,
  "out_html_dir": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/scratch",
  "plot_sections": "True",
  "match_collection": "NewPMS_combined_with_montage",
  "prestitched_stack": "2_sections_near_crack_fine_lam_1e3",
  "poststitched_stack": "2_sections_near_crack_fine_lam_1e3_omitted"
},
        "2D Montage Solver Input": {
  "render": {
    "host": "ibs-forrestc-ux1",
    "port": 8988,
    "owner": "test",
    "project": "em_montage_test",
    "client_scripts": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/dev/scripts/"
  },
  "verbose": 0,
  "last_section": 1015,
  "first_section": 1015,
  "solver_options": {
    "nbrs": 2,
    "Width": 3840,
    "debug": 0,
    "Height": 3840,
    "degree": 1,
    "pastix": {
      "ncpus": 8,
      "split": 1,
      "parms_fn": "/nrs/flyTEM/khairy/FAFB00v13/matlab_production_scripts/params_file.txt"
    },
    "pmopts": {
      "Transform": "Affine",
      "DesiredConfidence": 99.9,
      "MaximumRandomSamples": 5000,
      "PixelDistanceThreshold": 0.1,
      "NumRandomSamplingsMethod": "Desired confidence"
    },
    "solver": "backslash",
    "use_peg": 0,
    "verbose": 1,
    "sandwich": 0,
    "transfac": 1e-05,
    "min_tiles": 3,
    "nbrs_step": 1,
    "xs_weight": 0,
    "max_points": 200,
    "min_points": 5,
    "dir_scratch": "/allen/aibs/pipeline/image_processing/volume_assembly/scratch/solver_scratch",
    "distributed": 0,
    "edge_lambda": 0.005,
    "matrix_only": 0,
    "distribute_A": 16,
    "lambda_value": 1000,
    "outside_group": 0,
    "constrain_by_z": 0,
    "constraint_fac": 1000000000000000.0,
    "outlier_lambda": 1000,
    "disableValidation": 1,
    "filter_point_matches": 0
  },
  "solver_executable": "/allen/aibs/pipeline/image_processing/volume_assembly/EMAligner/dev/allen_templates/run_em_solver.sh",
  "source_collection": {
    "owner": "test",
    "stack": "input_raw_stack",
    "baseURL": "http://ibs-forrestc-ux1:8988/render-ws/v1",
    "project": "em_montage_test",
    "verbose": 0,
    "service_host": "ibs-forrestc-ux1:8988",
    "renderbinPath": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/dev/scripts/"
  },
  "target_collection": {
    "owner": "test",
    "stack": "render_modules_test",
    "baseURL": "http://ibs-forrestc-ux1:8988/render-ws/v1",
    "project": "em_montage_test",
    "verbose": 0,
    "service_host": "ibs-forrestc-ux1:8988",
    "renderbinPath": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/dev/scripts/"
  },
  "source_point_match_collection": {
    "owner": "test",
    "server": "http://ibs-forrestc-ux1:8988/render-ws/v1",
    "verbose": 0,
    "match_collection": "test_montage_collection"
  }
},
        "2D Montage Point Match Input": {
  "owner": "gayathri_MM2",
  "logdir": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch/sparkLogs/",
  "render": {
    "host": "http://em-131fs",
    "port": 8080,
    "owner": "gayathri",
    "project": "MM2",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
  },
  "jarfile": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-spark-client/target/render-ws-spark-client-0.3.0-SNAPSHOT-standalone.jar",
  "matchRod": 0.9,
  "pairJson": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch/rough/tilePairs/tile_pairs_mm2_montage_scape_test_z_1015_to_1035_dist_5.json",
  "SIFTsteps": 3,
  "className": "org.janelia.render.client.spark.SIFTPointMatchClient",
  "clipWidth": 800,
  "masterUrl": "spark://spark-master:7077",
  "sparkhome": "/allen/programs/celltypes/workgroups/em-connectomics/ImageProcessing/utils/spark/",
  "SIFTfdSize": 8,
  "clipHeight": 800,
  "collection": "mm2_rough_align_test",
  "baseDataUrl": "http://em-131fs:8080/render-ws/v1",
  "renderScale": 0.4,
  "SIFTmaxScale": 0.82,
  "SIFTminScale": 0.38,
  "matchMaxEpsilon": 20.0,
  "maxFeatureCacheGb": 15,
  "matchMaxNumInliers": 200,
  "matchMinNumInliers": 8,
  "matchMinInlierRatio": 0.0
},
        "Create Tile Pairs Input": {
  "maxZ": 1022,
  "minZ": 1015,
  "stack": "mm2_acquire_8bit_reimage",
  "render": {
    "host": "http://em-131fs",
    "port": 8998,
    "owner": "gayathri",
    "project": "MM2",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
  },
  "baseStack": "mm2_acquire_8bit_reimage",
  "output_dir": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch/montageTilepairs",
  "xyNeighborFactor": 0.9,
  "zNeighborDistance": 0,
  "excludeCornerNeighbors": "true",
  "excludeSameLayerNeighbors": "false",
  "excludeCompletelyObscuredTiles": "true"
},
        "Apply Lens Correction Input": {
  "refId": null,
  "render": {
    "host": "renderservice",
    "port": 8080,
    "owner": "samk",
    "project": "RENDERAPI_TEST",
    "client_scripts": "/path/to/scripts"
  },
  "zValues": [
    2266
  ],
  "pool_size": 10,
  "transform": {
    "type": "leaf",
    "className": "lenscorrection.NonLinearTransform",
    "dataString": ""
  },
  "close_stack": true,
  "input_stack": "test_noLC",
  "output_stack": "test_LC",
  "overwrite_zlayer": true
},
        "Apply MIPmaps Input": {
  "levels": 6,
  "render": {
    "host": "em-131fs",
    "port": 8998,
    "owner": "gayathri",
    "project": "MM2",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
  },
  "zValues": [
    1015
  ],
  "imgformat": "tif",
  "pool_size": 20,
  "mipmap_dir": "/net/aidc-isi1-prd/scratch/aibs/scratch",
  "input_stack": "mm2_acquire_8bit",
  "output_stack": "mm2_mipmap_test",
  "overwrite_zlayer": true
},
        "Generate MIPmaps Input": {
  "levels": 6,
  "method": "PIL",
  "render": {
    "host": "10.128.124.14",
    "port": 8998,
    "owner": "gayathri",
    "project": "MM2",
    "client_scripts": "/data/nc-em2/gayathrim/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
  },
  "zValues": [
    1015
  ],
  "imgformat": "tif",
  "force_redo": "True",
  "output_dir": "/net/aidc-isi1-prd/scratch/aibs/scratch",
  "input_stack": "mm2_acquire_8bit",
  "convert_to_8bit": "False"
},
        "Generate Render Stack Input": {
  "z": 1,
  "render": {
    "host": "em-131fs",
    "port": 8080,
    "owner": "russelt",
    "project": "RENDERAPI_TEST",
    "client_scripts": "/path/to/scripts"
  },
  "metafile": "/path/to/metafile.json",
  "pool_size": 10,
  "close_stack": false,
  "output_stack": "TEST_IMPORT_FROMMD",
  "overwrite_zlayer": true
},
        "Generate Lens Correction Input": {
  "outfile": "test_LC.json",
  "fiji_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/Fiji.app/ImageJ-linux64",
  "grid_size": 3,
  "heap_size": 20,
  "SIFT_params": {
    "steps": 3,
    "fdBins": 8,
    "fdSize": 4,
    "initialSigma": 1.6,
    "maxOctaveSize": 1200,
    "minOctaveSize": 800
  },
  "align_params": {
    "rod": 0.92,
    "dimension": 5,
    "lambdaVal": 0.01,
    "visualize": false,
    "maxEpsilon": 5.0,
    "regularize": false,
    "minNumInliers": 5,
    "clearTransform": true,
    "minInlierRatio": 0.0,
    "rejectIdentity": true,
    "tilesAreInPlace": true,
    "desiredModelIndex": 0,
    "identityTolerance": 5.0,
    "expectedModelIndex": 1,
    "multipleHypotheses": true,
    "maxIterationsOptimize": 2000,
    "maxPlateauWidthOptimize": 200
  },
  "project_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/lc_test_data/Wij_Set_594451332/594089217_594451332/",
  "manifest_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/lc_test_data/Wij_Set_594451332/594089217_594451332/_trackem_20170502174048_295434_5LC_0064_01_20170502174047_reference_0_.txt",
  "processing_directory": null
},
        "Generate Lens Correction Input": {
  "outfile": "test_LC.json",
  "fiji_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/Fiji.app/ImageJ-linux64",
  "grid_size": 3,
  "heap_size": 20,
  "SIFT_params": {
    "steps": 3,
    "fdBins": 8,
    "fdSize": 4,
    "initialSigma": 1.6,
    "maxOctaveSize": 1200,
    "minOctaveSize": 800
  },
  "align_params": {
    "rod": 0.92,
    "dimension": 5,
    "lambdaVal": 0.01,
    "visualize": false,
    "maxEpsilon": 5.0,
    "regularize": false,
    "minNumInliers": 5,
    "clearTransform": true,
    "minInlierRatio": 0.0,
    "rejectIdentity": true,
    "tilesAreInPlace": true,
    "desiredModelIndex": 0,
    "identityTolerance": 5.0,
    "expectedModelIndex": 1,
    "multipleHypotheses": true,
    "maxIterationsOptimize": 2000,
    "maxPlateauWidthOptimize": 200
  },
  "project_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/lc_test_data/Wij_Set_594451332/594089217_594451332/",
  "manifest_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/lc_test_data/Wij_Set_594451332/594089217_594451332/_trackem_20170502174048_295434_5LC_0064_01_20170502174047_reference_0_.txt",
  "processing_directory": null
},
"Generate Mesh Lens Correction Input": {
  "outfile": "test_LC.json",
  "fiji_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/Fiji.app/ImageJ-linux64",
  "grid_size": 3,
  "heap_size": 20,
  "SIFT_params": {
    "steps": 3,
    "fdBins": 8,
    "fdSize": 4,
    "initialSigma": 1.6,
    "maxOctaveSize": 1200,
    "minOctaveSize": 800
  },
  "align_params": {
    "rod": 0.92,
    "dimension": 5,
    "lambdaVal": 0.01,
    "visualize": false,
    "maxEpsilon": 5.0,
    "regularize": false,
    "minNumInliers": 5,
    "clearTransform": true,
    "minInlierRatio": 0.0,
    "rejectIdentity": true,
    "tilesAreInPlace": true,
    "desiredModelIndex": 0,
    "identityTolerance": 5.0,
    "expectedModelIndex": 1,
    "multipleHypotheses": true,
    "maxIterationsOptimize": 2000,
    "maxPlateauWidthOptimize": 200
  },
  "project_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/lc_test_data/Wij_Set_594451332/594089217_594451332/",
  "manifest_path": "/allen/programs/celltypes/workgroups/em-connectomics/samk/lc_test_data/Wij_Set_594451332/594089217_594451332/_trackem_20170502174048_295434_5LC_0064_01_20170502174047_reference_0_.txt",
  "processing_directory": null
},
        "Materialize Sections Input": {
  "owner": "russelt",
  "stack": "Secs_1015_1099_5_reflections_mml6_rough_affine_scaled",
  "width": 1024,
  "height": 1024,
  "jarfile": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/dev/render-ws-spark-client-standalone.jar",
  "project": "Reflections",
  "zValues": [
    1015,
    1017
  ],
  "maxLevel": 7,
  "className": "org.janelia.render.client.spark.betterbox.BoxClient",
  "masterUrl": "local[*,20]",
  "sparkhome": "/allen/aibs/pipeline/image_processing/volume_assembly/utils/spark/",
  "baseDataUrl": "http://em-131fs:8080/render-ws/v1",
  "driverMemory": "40g",
  "rootDirectory": "/allen/programs/celltypes/workgroups/em-connectomics/russelt/materialize_render/",
  "cleanUpPriorRun": "False",
  "maxImageCacheGb": 2.0
},
        "Make Montage Scapes Input": {
  "zend": 1022,
  "scale": 0.01,
  "render": {
    "host": "http://em-131fs",
    "port": 8080,
    "owner": "gayathri",
    "project": "Tests",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_latest/render-ws-java-client/src/main/scripts"
  },
  "zstart": 1020,
  "imgformat": "png",
  "pool_size": 20,
  "set_new_z": "False",
  "output_stack": "rough_test_downsample_montage_stack",
  "montage_stack": "rough_test_montage_stack",
  "image_directory": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/scratch"
},
        "Rough Alignment Solver Input": {
  "render": {
    "host": "http://em-131fs",
    "port": 8080,
    "owner": "gayathri",
    "project": "Tests",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_latest/render-ws-java-client/src/main/scripts"
  },
  "verbose": 0,
  "last_section": 1022,
  "first_section": 1020,
  "solver_options": {
    "nbrs": 5,
    "Width": 3840,
    "debug": 0,
    "Height": 3840,
    "degree": 1,
    "pastix": {
      "ncpus": 8,
      "split": 1,
      "parms_fn": "/allen/aibs/pipeline/image_processing/volume_assembly/EM_aligner/allen_templates/parms_file.txt"
    },
    "pmopts": {
      "Transform": "Affine",
      "DesiredConfidence": 99.9,
      "MaximumRandomSamples": 5000,
      "PixelDistanceThreshold": 0.1,
      "NumRandomSamplingsMethod": "Desired confidence"
    },
    "solver": "backslash",
    "use_peg": 0,
    "verbose": 1,
    "sandwich": 0,
    "transfac": 1e-15,
    "min_tiles": 2,
    "nbrs_step": 1,
    "xs_weight": 1,
    "max_points": 800,
    "min_points": 3,
    "close_stack": "True",
    "dir_scratch": "/allen/aibs/pipeline/image_processing/volume_assembly/scratch/solver_scratch",
    "distributed": 0,
    "edge_lambda": 100.0,
    "matrix_only": 0,
    "distribute_A": 16,
    "lambda_value": 100.0,
    "outside_group": 0,
    "constrain_by_z": 0,
    "constraint_fac": 1000000000000000.0,
    "outlier_lambda": 100,
    "disableValidation": 1,
    "filter_point_matches": 1
  },
  "solver_executable": "/allen/aibs/pipeline/image_processing/volume_assembly/EMAligner/dev/allen_templates/run_em_solver.sh",
  "source_collection": {
    "owner": "gayathri",
    "stack": "rough_test_downsample_montage_stack",
    "baseURL": "http://em-131fs:8080/render-ws/v1",
    "project": "Tests",
    "verbose": 0,
    "service_host": "em-131fs:8080"
  },
  "target_collection": {
    "owner": "gayathri",
    "stack": "rough_test_downsample_rough_stack",
    "baseURL": "http://em-131fs:8080/render-ws/v1",
    "project": "Tests",
    "verbose": 0,
    "service_host": "em-131fs:8080"
  },
  "source_point_match_collection": {
    "owner": "gayathri_MM2",
    "server": "http://em-131fs:8080/render-ws/v1",
    "verbose": 0,
    "match_collection": "rough_test"
  }
},
        "Rough Point Match Input": {
  "owner": "gayathri_MM2",
  "logdir": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch/sparkLogs/",
  "render": {
    "host": "http://em-131fs",
    "port": 8080,
    "owner": "gayathri",
    "project": "MM2",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
  },
  "jarfile": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-spark-client/target/render-ws-spark-client-0.3.0-SNAPSHOT-standalone.jar",
  "matchRod": 0.9,
  "pairJson": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch/rough/tilePairs/tile_pairs_mm2_montage_scape_test_z_1015_to_1035_dist_5.json",
  "SIFTsteps": 5,
  "className": "org.janelia.render.client.spark.SIFTPointMatchClient",
  "masterUrl": "spark://spark-master:7077",
  "sparkhome": "/allen/programs/celltypes/workgroups/em-connectomics/ImageProcessing/utils/spark/",
  "SIFTfdSize": 8,
  "collection": "mm2_rough_align_test",
  "baseDataUrl": "http://em-131fs:8080/render-ws/v1",
  "renderScale": 1.0,
  "SIFTmaxScale": 1.0,
  "SIFTminScale": 0.2,
  "matchMaxEpsilon": 20.0,
  "maxFeatureCacheGb": 3,
  "matchMaxNumInliers": 500,
  "matchMinNumInliers": 12,
  "matchMinInlierRatio": 0.0
},
        "Create Rough Tile Pairs Input": {
  "maxZ": 1022,
  "minZ": 1015,
  "stack": "mm2_acquire_8bit_reimage",
  "render": {
    "host": "http://em-131fs",
    "port": 8998,
    "owner": "gayathri",
    "project": "MM2",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_20170613/render-ws-java-client/src/main/scripts"
  },
  "baseStack": "mm2_acquire_8bit_reimage",
  "output_dir": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch/montageTilepairs",
  "xyNeighborFactor": 0.9,
  "zNeighborDistance": 3,
  "excludeCornerNeighbors": "true",
  "excludeSameLayerNeighbors": "true",
  "excludeCompletelyObscuredTiles": "true"
},
        "Apply Rough Alignment Input": {
  "maxZ": 1022,
  "minZ": 1020,
  "scale": 0.1,
  "render": {
    "host": "http://em-131fs",
    "port": 8080,
    "owner": "gayathri",
    "project": "Tests",
    "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_latest/render-ws-java-client/src/main/scripts"
  },
  "pool_size": 20,
  "set_new_z": "False",
  "lowres_stack": "rough_test_downsample_rough_stack",
  "output_stack": "rough_test_rough_stack",
  "montage_stack": "rough_test_montage_stack",
  "prealigned_stack": "rough_test_montage_stack",
  "tilespec_directory": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/scratch/rough/jsonFiles",
  "consolidate_trasnforms": "True"
}, "2D Montage Python Solver Input": {
  "pointmatch": {
    "host": "em-131fs",
    "name": "mm2_acquire_8bit_reimage_postVOXA_TEMCA2_Fine_rev1039",
    "port": 8080,
    "owner": "gayathri_MM2",
    "mongo_host": "em-131fs",
    "mongo_port": 27017,
    "db_interface": "mongo",
    "client_scripts": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/production/scripts",
    "collection_type": "pointmatch"
  },
  "solve_type": "montage",
  "close_stack": "True",
  "input_stack": {
    "host": "em-131fs",
    "name": "mm2_acquire_8bit_reimage_postVOXA_TEMCA2_rev1039",
    "port": 8080,
    "owner": "gayathri",
    "project": "MM2",
    "mongo_host": "em-131fs",
    "mongo_port": 27017,
    "db_interface": "mongo",
    "client_scripts": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/production/scripts",
    "collection_type": "stack"
  },
  "output_mode": "stack",
  "hdf5_options": {
    "output_dir": "/allen/programs/celltypes/workgroups/em-connectomics/danielk/example_output/",
    "chunks_per_file": -1
  },
  "last_section": 1020,
  "output_stack": {
    "host": "em-131fs",
    "name": "python_montage_results",
    "port": 8080,
    "owner": "danielk",
    "project": "Tests",
    "mongo_host": "em-131fs",
    "mongo_port": 27017,
    "db_interface": "render",
    "client_scripts": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/production/scripts",
    "collection_type": "stack"
  },
  "first_section": 1020,
  "regularization": {
    "default_lambda": 1000.0,
    "translation_factor": 1e-05
  },
  "transformation": "affine",
  "matrix_assembly": {
    "depth": 2,
    "npts_max": 500,
    "npts_min": 5,
    "inverse_dz": "True",
    "cross_pt_weight": 0.5,
    "montage_pt_weight": 1.0
  },
  "start_from_file": ""
}
    }"""
    
    input_dicts = json.loads(strategy_configurations.configs)
    p, _ = RunState.objects.update_or_create(name='PENDING')

    for k in input_dicts.keys():
        Configuration.objects.update_or_create(
            name=k,
            defaults={
                'configuration_type': 'strategy_config',
                'json_object': input_dicts[k],
                'content_object': p
                })

    return input_dicts

from workflow_engine.models.run_state import RunState
from workflow_engine.models.configuration import Configuration
