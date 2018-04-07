input_dict = {
    "masterUrl": "local[*,20]",
    "jarfile": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/dev/render-ws-spark-client-standalone.jar",
    "className": "org.janelia.render.client.spark.betterbox.BoxClient",
    "driverMemory": "40g",
    "sparkhome": "/allen/aibs/pipeline/image_processing/volume_assembly/utils/spark/",
    "baseDataUrl": "http://em-131fs:8080/render-ws/v1",
    "owner": "russelt",
    "project": "Reflections",
    "stack": "Secs_1015_1099_5_reflections_mml6_rough_affine_scaled",
    "rootDirectory": "/allen/programs/celltypes/workgroups/em-connectomics/russelt/materialize_render/",
    "cleanUpPriorRun": False,
    "maxImageCacheGb": 2.0,  # TODO see Eric's docs
    "zValues": [1015, 1017],
    "width": 1024,
    "height": 1024,
    "maxLevel": 7
}
