#!/bin/bash

pkill -9 -f "flower"
pkill -9 -f "ui_server"
pkill -9 -f "beat"
pkill -9 -f "manage"
pkill -9 -f "notebook"

export MOAB_AUTH=''

export BASE_DIR=/at_em_imaging_workflow

export PYTHONPATH=$PYTHONPATH:/EM_aligner_python

rm ${BASE_DIR}/logs/worker.log
rm ${BASE_DIR}/logs/ui.log
rm ${BASE_DIR}/logs/moab.log
rm ${BASE_DIR}/logs/monitor.log
rm ${BASE_DIR}/logs/workflow.log
rm ${BASE_DIR}/logs/result.log
rm ${BASE_DIR}/logs/beat.log
rm celerybeat.pid


export WORKFLOW_CONFIG_YAML=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.WORKFLOW_CONFIG_YAML)")
export APP_PACKAGE=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.APP_PACKAGE)")
export MESSAGE_QUEUE_HOST=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.MESSAGE_QUEUE_HOST)")
export MESSAGE_QUEUE_PORT=$(python -c "import ${DJANGO_SETTINGS_MODULE} as settings; print(settings.MESSAGE_QUEUE_PORT)")

python -m celery flower --url_prefix=flower --backend=rpc:// --broker=amqp://blue_sky_user:blue_sky_user@${MESSAGE_QUEUE_HOST}:${AMQP_PORT} -n flower@${APP_PACKAGE} &
DEBUG_LOG=${BASE_DIR}/logs/result.log python -m manage result_worker &
DEBUG_LOG=${BASE_DIR}/logs/worker.log python -m manage server_worker &
DEBUG_LOG=${BASE_DIR}/logs/workflow.log python -m manage workflow_worker &
DEBUG_LOG=${BASE_DIR}/logs/moab.log python -m manage moab_worker &
DEBUG_LOG=${BASE_DIR}/logs/monitor.log python -m manage monitor_worker &
DEBUG_LOG=${BASE_DIR}/logs/ui.log python -m workflow_engine.ui_server &
DEBUG_LOG=${BASE_DIR}/logs/nb.log python -m manage shell_plus --notebook &
sleep 20
DEBUG_LOG=${BASE_DIR}/logs/beat.log python -m celery -A workflow_engine.celery.moab_beat beat \
 --broker=amqp://blue_sky_user:blue_sky_user@${MESSAGE_QUEUE_HOST}:${MESSAGE_QUEUE_PORT}

