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
import pika
import simplejson as json
import os
from workflow_engine.models import RunState, Task, Workflow
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from development.models import *
from django.conf import settings
import logging
import traceback
from rendermodules.ingest.schemas import \
    example, EMMontageSetIngestSchema

_WORKFLOW_NAME='lens_correction_new'

def callback(ch, method, properties, body):
    Command.cb(ch, method, properties, body)


class Command(BaseCommand):
    _log = logging.getLogger(
        'development.mananagement.commands.ingest_reference_set')
    help = 'ingest handler for the message queue'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(
            'development.management.commands.ingest_reference_set').setLevel(
                logging.INFO)

        credentials = pika.PlainCredentials(
            settings.MESSAGE_QUEUE_USER,
            settings.MESSAGE_QUEUE_PASSWORD)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                settings.MESSAGE_QUEUE_HOST,
                settings.MESSAGE_QUEUE_PORT,
                '/',
                credentials))

        MQ = _WORKFLOW_NAME + '_ingest'
        Command._log.info("listening to queue: %s" % (MQ))
        channel = connection.channel()
        channel.queue_declare(queue=MQ,
                              durable=True)
        channel.basic_consume(callback,
                              queue=MQ,
                              no_ack=True)
        Command._log.info(
            ' [*] Waiting for messages. To exit press CTRL+C')

        channel.start_consuming()

    @classmethod
    def cb(cls, ch, method, properties, body):
        body = body.decode("utf-8") 
        Command._log.info(" [x] Received " + str(body))

        try:
            body_data = json.loads(body)
            Command._log.info(body_data)
            enqueued_object = cls.create_reference_set(body_data)
            Workflow.start_workflow(_WORKFLOW_NAME,
                                    enqueued_object)
        except Exception as e:
            Command._log.error(
                'Something went wrong: ' + traceback.print_exc(e))

    @classmethod
    def create_reference_set(cls, message):
        message_camera = message['acquisition_data']['camera']
        camera, _ = \
            Camera.objects.update_or_create(
                uid=message_camera['camera_id'],
                defaults={
                    'height': message_camera['height'],
                    'width': message_camera['width'],
                    'model': message_camera['model']})

        microscope_type, _ = \
            MicroscopeType.objects.update_or_create(
                name=message['acquisition_data']['microscope'])

        microscope, _ = \
            Microscope.objects.update_or_create(
                uid="DEADBEEF",
                defaults={
                    'microscope_type': microscope_type
                })

        storage_directory, metafile = \
            os.path.split(message['acquisition_data']['metafile'])

        reference_set, _ = ReferenceSet.objects.update_or_create(
                uid=message['reference_set_id'],
                defaults={
                    'storage_directory': storage_directory,
                    'workflow_state': 'Pending',
                    'camera': camera,
                    'microscope': microscope,
                    # 'project_path': '/example_data' # deprecated
                })

        return reference_set # TODO: return reference_set id to ingest client
