#!/bin/bash
export PYTHONPATH=/home/timf/at_em_imaging_workflow:/home/timf/blue_sky_workflow_engine:/home/timf/render-deploy/render_modules
export BLUE_SKY_PACKAGE=at_em_imaging_workflow
export BLUE_SKY_WORKER_NAME=pbs

export DJANGO_SETTINGS_MODULE=${BLUE_SKY_PACKAGE}.settings
export MESSAGE_QUEUE_HOST=ibs-timf-ux1
export WORKER_HOST=ibs-timf-ux1
export QMASTER_USERNAME=timf
export QMASTER_PASSWORD=''
#export PBS_FINISH_PATH=/home/timf/at_em_imaging_workflow/pbs_execution_finish.py

python -m celery -A execution_runner worker --loglevel=debug --concurrency=2 -Q ${BLUE_SKY_WORKER_NAME}_${BLUE_SKY_PACKAGE} -n ${BLUE_SKY_WORKER_NAME}_${BLUE_SKY_PACKAGE}@${WORKER_HOST} 2>&1 | tee ${BLUE_SKY_WORKER_NAME}_worker.log
