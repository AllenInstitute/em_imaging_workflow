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
from workflow_engine.models import RunState, Task, Workflow
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from development.models import *
from django.conf import settings
import logging
import traceback
from rendermodules.ingest.schemas import \
    example, EMMontageSetIngestSchema

_WORKFLOW_NAME='em_2d_montage_point_match'

def callback(ch, method, properties, body):
    Command.cb(ch, method, properties, body)


class Command(BaseCommand):
    _log = logging.getLogger(
        'development.mananagement.commands.ingest_worker')
    help = 'ingest handler for the message queue'

    # TODO: change this all over to use ingest_client
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(
            'development.management.commands.ingest_worker').setLevel(
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

        MQ = settings.INGEST_QUEUE_NAME
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
            em_montage_set = cls.create_em_render_set(body_data)
            Workflow.start_workflow(_WORKFLOW_NAME,
                                    em_montage_set)
        except Exception as e:
            Command._log.error(
                'Something went wrong: ' + traceback.print_exc(e))

    @classmethod
    def create_em_render_set(cls, message):
        Command._log.info('creating study')

        study, _ = Study.objects.update_or_create(
            name='DEADBEEF'
        )

        Command._log.info('creating specimen')
        specimen, _ = Specimen.objects.update_or_create(
            uid=message['section']['specimen'],
            defaults={
                'render_project': 'PROJECT Lorem Impsum',
                'render_owner': 'Lorem Imsum',
                'study': study
            })

        Command._log.info('creating section')
        section = Section.objects.create(
            z_index=message['section']['z_index'],
            metadata=None,
            specimen=specimen 
        )

        Command._log.info('creating load')
        load, _ = Load.objects.update_or_create(
            uid='DEADBEEF'
        )

        Command._log.info('creating sample holder')
        sample_holder, _ = SampleHolder.objects.update_or_create(
            uid=message['section']['sample_holder'],
            defaults={
                'imaged_sections_count': 0,
                'load': load
            })

        Command._log.info('creating em montage set')

        # if reference set id isn't specified,
        # montage set should still be created
        try:
            reference_set = ReferenceSet.objects.get(
                uid=message['reference_set_id'])
            reference_set_uid = reference_set.uid
        except ObjectDoesNotExist:
            reference_set = None
            reference_set_uid = None

        em_montage_set = EMMontageSet.objects.create(
            acquisition_date=message['acquisition_data']['acquisition_time'],
            overlap=message['acquisition_data']['overlap'],
            mipmap_directory=None,
            section=section,
            sample_holder=sample_holder,
            reference_set=reference_set,
            reference_set_uid=reference_set_uid,
            storage_directory=message['storage_directory']
        )
        Command._log.info(str(em_montage_set))

        return em_montage_set
