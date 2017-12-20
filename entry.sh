#!/bin/bash

export APP_NAME=at_em_imaging_workflow
mkdir -p logs
sleep 15
DEBUG_LOG=logs/makemigrations.log python -m manage makemigrations --noinput
sleep 15
DEBUG_LOG=logs/migrate.log python -m manage migrate  --noinput
sleep 15

export WORKFLOW_CONFIG_YAML=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.WORKFLOW_CONFIG_YAML)")

export DEBUG_LOG=logs/create_superuser.log
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('blue_sky_user', 'admin@example.com', 'blue_sky_user')" | python manage.py shell

export DEBUG_LOG=logs/superuser_pass.log
printf "blue_sky_user\nt@a.org\nblue_sky_user\n" | python manage.py createsuperuser

echo "reading workflows from workflow config yaml: " ${WORKFLOW_CONFIG_YAML}
DEBUG_LOG=logs/import_workflows.log python -m manage import_workflows ${WORKFLOW_CONFIG_YAML}

# Monitoring
python -m celery flower --backend=rpc:// --broker=amqp://blue_sky_user:blue_sky_user@${MESSAGE_QUEUE_HOST}:5672 -n flower@${APP_NAME} &

# TODO: switch worker client to use celery
#python -m celery -A workflow_client.worker_client worker --loglevel=debug --concurrency=2 -Q at_em_imaging_workflow -n at_em_worker@at_em_image_processing &

DEBUG_LOG=logs/server.log python -m manage server_worker&
DEBUG_LOG=logs/execution_worker.log python -m manage run_execution_worker&
DEBUG_LOG=logs/debug.log python -m manage runserver 0.0.0.0:8000&

while true; do sleep 2; done
