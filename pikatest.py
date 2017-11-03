#!/usr/bin/env python
import pika


credentials = pika.PlainCredentials(
    'blue_sky_user',
    'blue_sky_user')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        'ibs-timf-ux1',
        5672,
        '/',
        credentials))

channel = connection.channel()

channel.basic_publish(exchange='',
                      routing_key='em_2d_montage_ingest',
                      body='THISISATEST')
print(" [x] Sent 'Hello World!'")
