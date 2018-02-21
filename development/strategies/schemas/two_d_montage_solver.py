input_dict = {
    "render": {
        "host": "ibs-forrestc-ux1",
        "port": 8988,
        "owner": "test",
        "project": "em_montage_test",
        "client_scripts": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/dev/scripts/"
    },
    "first_section": 1015,
    "last_section": 1015,
    "solver_options": {
        "degree": 1,
        "solver": "backslash",
        "transfac": 1,
        "lambda": 0.005,
        "edge_lambda": 0.005,
        "nbrs": 2,
        "nbrs_step": 1,
        "xs_weight": 0,
        "min_points": 3,
        "max_points": 200,
        "filter_point_matches": 1,
        "outlier_lambda": 1000,
        "min_tiles": 3,
        "Width":3840,
        "Height":3840,
        "outside_group":0,
        "pastix": {
            "ncpus": 8,
            "parms_fn": "/nrs/flyTEM/khairy/FAFB00v13/matlab_production_scripts/params_file.txt",
            "split": 1
        },
        "matrix_only": 0,
        "distribute_A": 16,
        "dir_scratch": "/allen/aibs/pipeline/image_processing/volume_assembly/scratch/solver_scratch",
        "distributed": 0,
        "disableValidation": 1,
        "use_peg": 0,
        "pmopts": {
            "NumRandomSamplingsMethod": "Desired confidence",
            "MaximumRandomSamples": 5000,
            "DesiredConfidence": 99.9,
            "Transform":"Affine",
            "PixelDistanceThreshold": 0.1
        },
        "verbose": 1,
        "debug": 0,
        "constrain_by_z": 0,
        "sandwich": 0,
        "constraint_fac": 1e+15
    },
    "source_collection": {
        "owner": "test",
        "project": "em_montage_test",
        "stack": "input_raw_stack",
        "service_host": "ibs-forrestc-ux1:8988",
        "baseURL": "http://ibs-forrestc-ux1:8988/render-ws/v1",
        "renderbinPath": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/dev/scripts/",
        "verbose": 0
    },
    "target_collection": {
        "owner": "test",
        "project": "em_montage_test",
        "stack": "render_modules_test",
        "service_host": "ibs-forrestc-ux1:8988",
        "baseURL": "http://ibs-forrestc-ux1:8988/render-ws/v1",
        "renderbinPath": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/dev/scripts/",
        "verbose": 0
    },
    "source_point_match_collection": {
        "server": "http://ibs-forrestc-ux1:8988/render-ws/v1",
        "owner": "test",
        "match_collection": "test_montage_collection",
        "verbose": 0
    },
    "verbose": 0,
    "solver_executable": "/allen/aibs/pipeline/image_processing/volume_assembly/EMAligner/dev/allen_templates/run_em_solver.sh"
}