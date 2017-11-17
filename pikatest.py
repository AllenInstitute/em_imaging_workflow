#!/usr/bin/env python
from rendermodules.ingest.schemas import example as message_body_data
from workflow_client.ingest_client import IngestClient

MESSAGE_QUEUE_HOST='ibs-timf-ux1.corp.alleninstitute.org'
# MESSAGE_HOST='em-131db.corp.alleninstitute.org'

MESSAGE_QUEUE_USER='blue_sky_user'
MESSAGE_QUEUE_PASSWORD='blue_sky_user'
MESSAGE_QUEUE_PORT = 5672
MESSAGE_QUEUE_EXCHANGE = ''
MESSAGE_QUEUE_ROUTE='em_2d_montage_ingest'

with IngestClient(MESSAGE_QUEUE_HOST,
                  MESSAGE_QUEUE_PORT,
                  MESSAGE_QUEUE_USER,
                  MESSAGE_QUEUE_PASSWORD,
                  MESSAGE_QUEUE_EXCHANGE,
                  MESSAGE_QUEUE_ROUTE) as ic:
    for i in range(0, 1):
        message_body_data['reference_set_id'] = 'WHATEVER%d' % (i)
        ic.send_as_json(message_body_data)
