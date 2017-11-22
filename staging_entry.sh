#!/bin/bash
sleep 10

export APP_NAME=at_em_imaging_workflow

export DEBUG_LOG=logs/makemigrations.log
python manage.py makemigrations

export DEBUG_LOG=logs/migrate.log
python manage.py migrate --noinput

sleep 10

export DEBUG_LOG=logs/create_superuser.log

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('blue_sky_user', 'admin@example.com', 'blue_sky_user')" | python manage.py shell

export DEBUG_LOG=logs/superuser_pass.log
printf "blue_sky_user\nt@a.org\nblue_sky_user\n" | python manage.py createsuperuser

python -m celery flower --backend=rpc:// --broker=amqp://blue_sky_user:blue_sky_user@${MESSAGE_QUEUE_HOST}:5672 -n flower@${APP_NAME} &

export DEBUG_LOG=logs/import_workflows.log
python -m manage import_workflows tests/workflows/dev.yml

# python -m celery -A workflow_client.worker_client worker --loglevel=debug --concurrency=2 -Q at_em_imaging_workflow -n at_em_worker@at_em_image_processing &
#python manage.py ingest_worker &
#python manage.py ingest_reference_set &
#python -m manage ingest &

export DEBUG_LOG=logs/server.log
python -m manage server_worker&

export DEBUG_LOG=logs/execution_worker.log
python -m manage run_execution_worker&

export DEBUG_LOG=logs/debug.log
python -m manage runserver 0.0.0.0:8000
