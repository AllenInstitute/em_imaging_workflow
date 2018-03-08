input_dict = {
    "input_stack": "TEST_IMPORT_FROMMD",
    "output_stack": "TEST_redmml",
    "pool_size": 10,
    "render": {
        "host": "em-131fs",
        "port": 8080,
        "owner": "russelt",
        "project": "RENDERAPI_TEST",
        "client_scripts": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/production/scripts/"
    },
    "close_stack": False,
    "overwrite_zlayer": True,
    "z": 1,
    "new_mipmap_directories": [{
        "level": 0,
        "directory": "/allen/programs/celltypes/production/"
        }]
}
