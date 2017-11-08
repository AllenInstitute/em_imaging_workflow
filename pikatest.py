#!/usr/bin/env python
from rendermodules.ingest.schemas import example as ex
import pika
import simplejson as json

credentials = pika.PlainCredentials(
    'blue_sky_user',
    'blue_sky_user')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        'em-131db',
        5672,
        '/',
        credentials))

channel = connection.channel()

body_text = json.dumps(ex)

channel.basic_publish(exchange='',
                      routing_key='em_2d_montage_ingest',
                      body=body_text)
print(" [x] Sent '%s'" % (body_text))
