#!/usr/bin/env python
from rendermodules.ingest.schemas import example as ex
import pika
import simplejson as json

# MESSAGE_HOST='ibs-timf-ux1'
MESSAGE_HOST='em-131db.corp.alleninstitute.org'

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
                          routing_key='em_2d_montage_ingest',
                          body=body_text)
    print(" [x] Sent '%s'" % (body_text))

if __name__ == '__main__':
    send()
