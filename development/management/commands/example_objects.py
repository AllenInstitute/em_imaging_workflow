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
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from development.models import *
from workflow_engine.models import JobQueue
import logging

_log = logging.getLogger(
    'development.mananagement.commands.example_objects')


class Command(BaseCommand):
    help = 'Generate Example Objects (Microscope, Camera, etc.)'

    @classmethod
    def example_reference_set(cls):
        camera, _ = \
            Camera.objects.update_or_create(
                uid="DEADBEEF")

        microscope_type, _ = \
            MicroscopeType.objects.update_or_create(
                name="DEADBEEF")

        microscope, _ = \
            Microscope.objects.update_or_create(
                uid="DEADBEEF",
                defaults={
                    'microscope_type': microscope_type
                })

        reference_set, _ = \
            ReferenceSet.objects.update_or_create(
                uid="DEADBEEF",
                defaults={
                    'storage_directory': '/example_data',
                    'workflow_state': 'Lorem Ipsum',
                    'camera': camera,
                    'microscope': microscope,
                    'project_path': '/example_data'
                })

        return reference_set

    @classmethod
    def example_em_montage_set(cls):
        _log.info('creating study')
        study, _ = Study.objects.update_or_create(
            name='DEADBEEF',
            defaults={
                'storage_directory': '/study/directory'
            })

        _log.info('creating specimen')
        specimen, _ = Specimen.objects.update_or_create(
            uid='DEADBEEF',
            defaults={
                'render_project': 'PROJECT Lorem Impsum',
                'render_owner': 'Lorem Imsum',
                'study': study
            })

        _log.info('creating section')
        section, _ = Section.objects.update_or_create(
            id='12345',
            defaults={
                'z_index': 98765,
                'metadata': None,
                'specimen': specimen 
                # TODO: many-to-many fields
                # 'chucks': None,    # TODO ???
                # 'sample_holders'
            })

        _log.info('creating load')
        load, _ = Load.objects.update_or_create(
            uid='DEADBEEF'
        )


        _log.info('creating sample holder')
        sample_holder, _ = SampleHolder.objects.update_or_create(
            uid='DEADBEEF',
            defaults={
                'imaged_sections_count': 0,
                'load': load
            })

        _log.info('creating em montage set')
        example_reference_set = cls.example_reference_set()
        em_montage_set, _ = EMMontageSet.objects.update_or_create(
            uid="DEADBEEF",
            defaults={
                'acquisition_date': None,
                'mipmap_directory': '/mip/map/directory',
                'section': section,
                'sample_holder': sample_holder,
                'reference_set': example_reference_set,
                'reference_set_uid': example_reference_set.uid
         
            })

    @classmethod
    def fix_nathans_queue(cls):
        # fix strategy and enqueued object classes for existing workflow
        apply_montage_set_queue, _ = \
            JobQueue.objects.update_or_create(
                name='apply_to_previously_uploaded_montage_sets_queue',
                defaults={
                    'description': 'N/A',
                    'job_strategy_class': 'development.strategies.' + \
                        'apply_to_previously_uploaded_' + \
                        'montage_sets_strategy.' + \
                        'ApplyToPreviouslyUploadedMontageSetsStrategy',
                    'enqueued_object_class': 'development.models.' + \
                        'ReferenceSet'
                })
        generate_lens_correction_transform_queue, _ = \
            JobQueue.objects.update_or_create(
                name='generate_lens_correction_transform_queue',
                defaults={
                    'description': 'N/A',
                    'job_strategy_class': 'development.strategies.' + \
                        'generate_lens_correction_transform_strategy.' + \
                        'GenerateLensCorrectionTransformStrategy',
                    'enqueued_object_class': 'development.models.' + \
                        'ReferenceSet'
                })

    def add_arguments(self, parser):
        # parser.add_argument('file')
        pass

    def handle(self, *args, **options):
        # file_path = options['file']
        try:
            self.__class__.example_reference_set()
        except Exception as e:
            _log.error('Something went wrong: ' + str(e))

        try:
            self.__class__.example_em_montage_set()
        except Exception as e:
            _log.error('Something went wrong: ' + str(e))

        try:
            self.__class__.fix_nathans_queue()
        except Exception as e:
            _log.error('Something went wrong: ' + str(e))

