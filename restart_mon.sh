#!/bin/bash

pkill -9 -f "monitor_worker"

export BASE_DIR=/at_em_imaging_workflow

rm ${BASE_DIR}/logs/monitor.log
rm ${BASE_DIR}/logs/beat.log

export WORKFLOW_CONFIG_YAML=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.WORKFLOW_CONFIG_YAML)")
export APP_PACKAGE=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.APP_PACKAGE)")
export MESSAGE_QUEUE_HOST=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.MESSAGE_QUEUE_HOST)")
export MESSAGE_QUEUE_PORT=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.MESSAGE_QUEUE_PORT)")

DEBUG_LOG=${BASE_DIR}/logs/monitor.log python -m manage monitor_worker &
#DEBUG_LOG=${BASE_DIR}/logs/monitor_beat.log python -m celery -A development.management.commands.monitor_worker beat \
# --broker=amqp://blue_sky_user:blue_sky_user@${MESSAGE_QUEUE_HOST}:${MESSAGE_QUEUE_PORT} &

