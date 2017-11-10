#!/bin/bash
export PYTHONPATH=/at_em_imaging_workflow:/blue_sky_workflow_engine:/render-modules:/schema_package
export MESSAGE_QUEUE_HOST=ibs-timf-ux1

python -m celery -A execution_runner worker --loglevel=debug --concurrency=2 -Q spark_at_em_imaging_workflow -n at_em_worker_spark@at_em_image_processing
