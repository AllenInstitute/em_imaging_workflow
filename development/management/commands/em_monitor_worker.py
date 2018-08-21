# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2017. Allen Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Redistributions for commercial purposes are not permitted without the
# Allen Institute's written permission.
# For purposes of this license, commercial purposes is the incorporation of the
# Allen Institute's software into anything for which you will charge fees or
# other compensation. Contact terms@alleninstitute.org for commercial licensing
# opportunities.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
import celery
import django; django.setup()
from django.core.management.base import BaseCommand
from django.conf import settings

from workflow_client.client_settings import configure_worker_app
from celery import signature
import logging.config


app = celery.Celery('at_em_imaging_workflow.celery.monitor_tasks')
configure_worker_app(app, settings.APP_PACKAGE)
app.conf.imports = (
    'at_em_imaging_workflow.celery.monitor_tasks',
)

update_job_grid_json_signature = signature(
    'at_em_imaging_workflow.celery.monitor_tasks'
    '.update_job_grid_json')
update_job_grid_json_signature.set(
    broker_connection_timeout=10,
    broker_connection_retry=False,
    delivery_mode='transient',  # see celery issue 3620
    # exchange=_EXCHANGE,
    # routing_key='monitor',
    queue='monitor_at_em_imaging_workflow') # settings.MOAB_MESSAGE_QUEUE_NAME)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        300.0,
        update_job_grid_json_signature)


@celery.signals.after_setup_task_logger.connect
def after_setup_celery_task_logger(logger, **kwargs):
    logging.config.dictConfig(settings.LOGGING)


class Command(BaseCommand):
    help = 'monitor handler for the message queues'

    def handle(self, *args, **options):
        app_name = settings.APP_PACKAGE

        app.start(argv=[
            'celery', 
            '-A',
            'development.management.commands.monitor_worker',
            'worker',
            '--concurrency=1',
            '--heartbeat-interval=30',
            '-Q', 'at_em_broadcast', # settings.MONITOR_MESSAGE_QUEUE_NAME,
            '-n', 'monitor@' + app_name])
