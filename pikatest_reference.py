#!/usr/bin/env python
#from rendermodules.ingest.schemas import example as message_body_data
from workflow_client.ingest_client import IngestClient

MESSAGE_QUEUE_HOST='ibs-timf-ux1.corp.alleninstitute.org'
# MESSAGE_QUEUE_HOST='em-131db.corp.alleninstitute.org'
MESSAGE_QUEUE_USER='blue_sky_user'
MESSAGE_QUEUE_PASSWORD='blue_sky_user'
MESSAGE_QUEUE_PORT = 5672
MESSAGE_QUEUE_EXCHANGE = ''
MESSAGE_QUEUE_ROUTE='lens_correction_new_ingest'

message_body_data = {
    "reference_set_id": "DEADBEEF",
    "acquisition_data": {
    "microscope": "temca2",
        "camera": {
            "camera_id": "4450428",
            "height": 3840,
            "width": 3840,
            "model": "Ximea CB200MG"
        },
        "overlap": 0.07,
        "acquisition_time": "2017-08-29T13:01:46",
        "metafile": "/allen/aibs/pipeline/image_processing/volume_assembly/dataimport_test_data/_metadata_20170829130146_295434_5LC_0064_01_redo_001050_0_.json"
    }
}

with IngestClient(MESSAGE_QUEUE_HOST,
                  MESSAGE_QUEUE_PORT,
                  MESSAGE_QUEUE_USER,
                  MESSAGE_QUEUE_PASSWORD,
                  MESSAGE_QUEUE_EXCHANGE,
                  MESSAGE_QUEUE_ROUTE) as ic:
    for i in range(0, 1):
        message_body_data['reference_set_id'] = 'WHATEVER%d' % (i)
        ic.send_as_json(message_body_data)
