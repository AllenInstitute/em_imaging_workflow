input_dict = {
    "render": {
        "host": "http://em-131fs",
        "port": 8080,
        "owner": "gayathri",
        "project": "Tests",
        "client_scripts": "/allen/programs/celltypes/workgroups/em-connectomics/gayathrim/nc-em2/Janelia_Pipeline/render_latest/render-ws-java-client/src/main/scripts"
    },
    "first_section": 1020,
    "last_section": 1022,
    "solver_options": {
        "degree": 1,
        "solver": "backslash",
        "transfac": 1e-15,
        "lambda_value": 100.0,
        "edge_lambda": 100.0,
        "nbrs": 5,
        "nbrs_step": 1,
        "xs_weight": 1,
        "min_points": 3,
        "max_points": 800,
        "filter_point_matches": 1,
        "outlier_lambda": 100,
        "min_tiles": 2,
        "Width":3840,
        "Height":3840,
        "outside_group":0,
        "close_stack":"True",
        "pastix": {
            "ncpus": 8,
            "parms_fn": "/allen/aibs/pipeline/image_processing/volume_assembly/EM_aligner/allen_templates/parms_file.txt",
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
        "owner": "gayathri",
        "project": "Tests",
        "stack": "rough_test_downsample_montage_stack",
        "service_host": "em-131fs:8080",
        "baseURL": "http://em-131fs:8080/render-ws/v1",
        "verbose": 0
    },
    "target_collection": {
        "owner": "gayathri",
        "project": "Tests",
        "stack": "rough_test_downsample_rough_stack",
        "service_host": "em-131fs:8080",
        "baseURL": "http://em-131fs:8080/render-ws/v1",
        "verbose": 0
    },
    "source_point_match_collection": {
        "server": "http://em-131fs:8080/render-ws/v1",
        "owner": "gayathri_MM2",
        "match_collection": "rough_test",
        "verbose": 0
    },
    "verbose": 0,
    "solver_executable": "/allen/aibs/pipeline/image_processing/volume_assembly/EMAligner/dev/allen_templates/run_em_solver.sh"
}