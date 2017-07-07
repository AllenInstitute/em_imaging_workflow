from celery import Celery
import os
import pika

MESSAGE_QUEUE_HOST = '10.128.26.155'

app = Celery('execution_runner', backend='rpc://', broker='pyamqp://guest@' + MESSAGE_QUEUE_HOST + '//')

app.conf.task_default_queue = 'celery'

SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1

@app.task
def run_celery_task(full_executable, task_id, logfile):

	connection = pika.BlockingConnection(pika.ConnectionParameters(host=MESSAGE_QUEUE_HOST))
	channel = connection.channel()

	exit_code = SUCCESS_EXIT_CODE

	channel.queue_declare(queue='tasks')
	channel.basic_publish(exchange='', routing_key='tasks', body='RUNNING,' + str(task_id))
	
	try:
		exit_code = os.system(full_executable)

		if exit_code == SUCCESS_EXIT_CODE:
			channel.basic_publish(exchange='', routing_key='tasks', body='FINISHED_EXECUTION,' + str(task_id))

			with open(logfile, "a") as log:
				log.write("SUCCESS - execution finished successfully for task " + str(task_id))

		else:
			channel.basic_publish(exchange='', routing_key='tasks', body='FAILED_EXECUTION,' + str(task_id))

			with open(logfile, "a") as log:
				log.write("FAILURE - execution failed for task " + str(task_id))

	except Exception as e:
		exit_code = ERROR_EXIT_CODE
		channel.basic_publish(exchange='', routing_key='tasks', body='FAILED_EXECUTION,' + str(task_id))

	return exit_code

	connection.close()

