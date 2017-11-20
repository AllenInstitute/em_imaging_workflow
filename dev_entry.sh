#!/bin/bash
sleep 20
export PYTHONPATH=/at_em_imaging_workflow:/blue_sky_workflow_engine:/render-modules:/schema_package
export DJANGO_SETTINGS_MODULE=at_em_imaging_workflow.settings
export MESSAGE_QUEUE_HOST=ibs-timf-ux1.corp.alleninstitute.org

python manage.py makemigrations
python manage.py migrate  --noinput
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('blue_sky_user', 'admin@example.com', 'blue_sky_user')" | python manage.py shell
printf "blue_sky_user\nt@a.org\nblue_sky_userMan\n" | python manage.py createsuperuser
python manage.py import_workflows tests/workflows/dev.yml
python -m celery flower --backend=rpc:// --broker=amqp://blue_sky_user:blue_sky_user@${MESSAGE_QUEUE_HOST}:5672 -n flower@at_em_image_processing &
#python -m celery -A workflow_client.worker_client worker --loglevel=debug --concurrency=2 -Q at_em_imaging_workflow -n at_em_worker@at_em_image_processing &
# python manage.py ingest_worker &
# python manage.py ingest_reference_set &
python manage.py ingest &
python manage.py run_execution_worker&
python manage.py runserver 0.0.0.0:8000
