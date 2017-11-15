#!/usr/bin/env python
import sys
import pika


MESSAGE_QUEUE_NAME = 'at_em_imaging_workflow'
CELERY_MESSAGE_QUEUE_NAME = 'celery_at_em_imaging_workflow'
MESSAGE_QUEUE_HOST = 'ibs-timf-ux1'
MESSAGE_QUEUE_USER = 'blue_sky_user'
MESSAGE_QUEUE_PASSWORD = 'blue_sky_user'
MESSAGE_QUEUE_PORT = 5672

FIRST_ARG = 1
SECOND_ARG = 2
SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1


if __name__ == '__main__':
    exit_code = int(sys.argv[FIRST_ARG])
    task_id = sys.argv[SECOND_ARG]

    credentials = pika.PlainCredentials(MESSAGE_QUEUE_USER,
                                        MESSAGE_QUEUE_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            MESSAGE_QUEUE_HOST,
            MESSAGE_QUEUE_PORT,
            '/',
            credentials))
    channel = connection.channel()
    channel.queue_declare(queue=CELERY_MESSAGE_QUEUE_NAME,
                          durable=True)

    if exit_code == SUCCESS_EXIT_CODE:
        channel.basic_publish(exchange='',
        routing_key=CELERY_MESSAGE_QUEUE_NAME,
        body='FINISHED_EXECUTION,' + str(task_id))
    else:
        channel.basic_publish(
            exchange='',
            routing_key=CELERY_MESSAGE_QUEUE_NAME,
            body='FAILED_EXECUTION,' + str(task_id))
    
