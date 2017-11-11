#!/bin/bash
sleep 20
export PYTHONPATH=/at_em_imaging_workflow:/blue_sky_workflow_engine:/render-modules:/schema_package
export DJANGO_SETTINGS_MODULE=at_em_imaging_workflow.staging_settings
export MESSAGE_QUEUE_HOST=em-131db

python manage.py makemigrations
python manage.py migrate 

echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'WhateverMan')" | python manage.py shell

printf "admin\nt@a.org\nWhateverMan\n" | python manage.py createsuperuser
python manage.py import_workflows tests/workflows/dev.yml
python -m celery flower --backend=rpc:// --broker=amqp://blue_sky_user:blue_sky_user@message_queue:5672 -n flower@at_em_image_processing &
# python -m celery -A execution_runner worker --loglevel=debug --concurrency=2 -Q at_em_imaging_workflow -n at_em_worker@at_em_image_processing &
python manage.py ingest_worker &
python manage.py ingest_reference_set &
export DJANGO_SETTINGS_MODULE=at_em_imaging_workflow.staging_server_worker_settings
python manage.py run_execution_worker&
export DJANGO_SETTINGS_MODULE=at_em_imaging_workflow.staging_settings
python manage.py runserver 0.0.0.0:8000
