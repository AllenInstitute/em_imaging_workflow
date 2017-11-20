#!/bin/bash
export BLUE_SKY_PACKAGE=at_em_imaging_workflow
export DJANGO_SETTINGS_MODULE=${BLUE_SKY_PACKAGE}.settings
export MESSAGE_QUEUE_HOST=ibs-timf-ux1.corp.alleninstitute.org
export WORKER_HOST=ibs-timf-ux1.corp.alleninstitute.org

export QMASTER_HOST=hpc-login
export QMASTER_USERNAME=timf
export QMASTER_PASSWORD=''
export QMASTER_PORT=22

export BLUE_SKY_WORKER_NAME=pbs
python -m celery -A workflow_client.worker_client worker --loglevel=debug --concurrency=2 \
 -Q ${BLUE_SKY_WORKER_NAME}_${BLUE_SKY_PACKAGE} \
 -n ${BLUE_SKY_WORKER_NAME}_${BLUE_SKY_PACKAGE}@${WORKER_HOST} 2>&1 | \
 tee /data/aibstemp/timf/example_data/${BLUE_SKY_WORKER_NAME}_worker.log &
unset DJANGO_SETTINGS_MODULE

export BLUE_SKY_WORKER_NAME=local
python -m celery -A workflow_client.worker_client worker --loglevel=debug --concurrency=2 \
 -Q ${BLUE_SKY_PACKAGE} \
 -n ${BLUE_SKY_WORKER_NAME}_${BLUE_SKY_PACKAGE}@${WORKER_HOST} 2>&1 | \
 tee /data/aibstemp/timf/example_data/${BLUE_SKY_WORKER_NAME}_worker.log
