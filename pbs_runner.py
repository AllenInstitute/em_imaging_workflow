from celery import Celery
import os
import pika

MESSAGE_QUEUE_HOST = 'message_queue'
MESSAGE_QUEUE_NAME = 'at_em_imaging_workflow'
MESSAGE_QUEUE_USER = 'blue_sky_user'
MESSAGE_QUEUE_PASSWORD = 'blue_sky_user'

app = Celery('pbs_runner', backend='rpc://', broker='pyamqp://' + str(MESSAGE_QUEUE_USER) + ':' + str(MESSAGE_QUEUE_PASSWORD) + '@' + MESSAGE_QUEUE_HOST + '//')
app.conf.task_default_queue = 'pbs' + MESSAGE_QUEUE_NAME

SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
FIRST = 0

@app.task
def run_pbs_celery_task(pbs_file, task_id):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=MESSAGE_QUEUE_HOST))
    channel = connection.channel()

    exit_code = SUCCESS_EXIT_CODE

    channel.queue_declare(queue='tasks')
    channel.basic_publish(exchange='', routing_key='tasks', body='RUNNING,' + str(task_id))

    try:
        executable = 'qsub ' + str(pbs_file)
        pbs_id = os.popen(executable).readlines()[FIRST].strip().replace(".corp.alleninstitute.org", "")
        channel.basic_publish(exchange='', routing_key='tasks', body='PBS_ID,' + str(task_id) + ',' +  str(pbs_id))

    except Exception as e:
        print('something went wrong')

    return exit_code

    connection.close()

@app.task
def cancel_task(pbs_id):
    try:
        executable = 'qdel ' + str(pbs_id)
        exit_code = os.system(executable)
    except Exception as e:
        print('something went wrong')
