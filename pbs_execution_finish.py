
#!/usr/bin/env python
import sys
import pika


MESSAGE_QUEUE_NAME = 'at_em_imaging_workflow'
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

	connection = pika.BlockingConnection(pika.ConnectionParameters(host=MESSAGE_QUEUE_HOST))
	channel = connection.channel()
	channel.queue_declare(queue=MESSAGE_QUEUE_NAME)

	if exit_code == SUCCESS_EXIT_CODE:
		channel.basic_publish(exchange='', routing_key=MESSAGE_QUEUE_NAME, body='FINISHED_EXECUTION,' + str(task_id))
	else:
		channel.basic_publish(exchange='', routing_key=MESSAGE_QUEUE_NAME, body='FAILED_EXECUTION,' + str(task_id))
	