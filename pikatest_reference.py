#!/usr/bin/env python
#from rendermodules.ingest.schemas import example as ex
import pika
import simplejson as json

MESSAGE_HOST='ibs-timf-ux1'
#MESSAGE_HOST='em-131db.corp.alleninstitute.org'

ex = {
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
        "acquisition_time": "2017-08-29T13:01:46"
    }
}


def send():
    credentials = pika.PlainCredentials(
        'blue_sky_user',
        'blue_sky_user')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            MESSAGE_HOST,
            5672,
            '/',
            credentials))

    channel = connection.channel()

    body_text = json.dumps(ex)

    channel.basic_publish(exchange='',
                          routing_key='lens_correction_new_ingest',
                          body=body_text)
    print(" [x] Sent '%s'" % (body_text))

if __name__ == '__main__':
    send()
