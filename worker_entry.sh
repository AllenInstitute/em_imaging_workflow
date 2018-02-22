#!/bin/bash
export BLUE_SKY_PACKAGE=at_em_imaging_workflow
export QMASTER_HOST='hpc-login.corp.alleninstitute.org'
export QMASTER_PORT=22

export BLUE_SKY_WORKER_NAME=pbs
python -m celery -A workflow_client.worker_client worker \
 --loglevel=debug --concurrency=10 \
 -Q ${BLUE_SKY_WORKER_NAME}_${BLUE_SKY_PACKAGE} \
 -n ${BLUE_SKY_WORKER_NAME}_${BLUE_SKY_PACKAGE}@${WORKER_HOST} 2>&1 | \
 tee /at_em_imaging_workflow/logs/${BLUE_SKY_WORKER_NAME}_worker.log &

#unset DJANGO_SETTINGS_MODULE
#export BLUE_SKY_WORKER_NAME=local
#python -m celery -A workflow_client.worker_client worker \
# --loglevel=debug --concurrency=2 \
# -Q ${BLUE_SKY_PACKAGE} \
# -n ${BLUE_SKY_WORKER_NAME}_${BLUE_SKY_PACKAGE}@${WORKER_HOST} 2>&1 | \
# tee /at_em_imaging_workflow/logs/${BLUE_SKY_WORKER_NAME}_worker.log
