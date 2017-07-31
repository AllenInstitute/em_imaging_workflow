
#!/usr/bin/env python
import sys
import pika

FIRST_ARG = 1
SECOND_ARG = 2
MESSAGE_QUEUE_HOST = 'TODO_SET_MESSAGE_QUEUE_HOST'
MESSAGE_QUEUE_NAME = 'TODO_SET_MESSAGE_QUEUE_NAME'
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
	