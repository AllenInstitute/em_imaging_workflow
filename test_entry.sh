#!/bin/bash

export APP_NAME=at_em_imaging_workflow
mkdir -p logs
sleep 15
DEBUG_LOG=logs/migrate.log python -m manage migrate  --noinput
sleep 15

export WORKFLOW_CONFIG_YAML=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.WORKFLOW_CONFIG_YAML)")

export DEBUG_LOG=logs/create_superuser.log
echo "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('blue_sky_user', 'admin@example.com', 'blue_sky_user')" | python manage.py shell

export DEBUG_LOG=logs/superuser_pass.log
printf "blue_sky_user\nt@a.org\nblue_sky_user\n" | python manage.py createsuperuser

/bin/bash run_testserver.sh&

while true; do sleep 2; done
