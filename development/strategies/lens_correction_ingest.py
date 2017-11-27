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
import os
from workflow_engine.strategies.ingest_strategy import IngestStrategy
from development.models.camera import Camera
from development.models.microscope_type import MicroscopeType 
from development.models.microscope import Microscope
from development.models.reference_set import ReferenceSet
import logging
import traceback
from rendermodules.ingest.schemas import \
    example, ReferenceSetIngestSchema

class LensCorrectionIngest(IngestStrategy):
    _log = logging.getLogger('development.strategies.lens_correction_ingest')

    def get_workflow_name(self):
        LensCorrectionIngest._log.info('get_workflow_name')

        return 'lens_correction_new'

    def create_camera(self, message_camera):
        camera, _ = \
            Camera.objects.update_or_create(
                uid=message_camera['camera_id'],
                defaults={
                    'height': message_camera['height'],
                    'width': message_camera['width'],
                    'model': message_camera['model']})

        return camera

    def create_microscope(self, message_microscope):
        scope_type, _ = \
            MicroscopeType.objects.update_or_create(
                name=message_microscope)

        microscope, _ = \
            Microscope.objects.update_or_create(
                uid="DEADBEEF",
                defaults={
                    'microscope_type': scope_type
                })

        return microscope

    def create_enqueued_object(self, message):
        LensCorrectionIngest._log.info('create_enqueued_object')

        camera = self.create_camera(
            message['acquisition_data']['camera'])
        microscope = self.create_microscope(
            message['acquisition_data']['microscope'])

        metafile = message['metafile']
        manifest_path = message['manifest_path']

        reference_set, _ = ReferenceSet.objects.update_or_create(
                uid=message['reference_set_id'],
                defaults={
                    'storage_directory': message['storage_directory'],
                    'metafile': metafile,
                    'workflow_state': 'Pending',
                    'camera': camera,
                    'microscope': microscope,
                    # 'project_path': '/example_data', # deprecated
                    'manifest_path': manifest_path,
                    'metafile': metafile
                })

        return reference_set # TODO: return reference_set id to ingest client


    def generate_response(self, ref_set):
        LensCorrectionIngest._log.info('generate_response')

        return {
            'reference_set_id': ref_set.uid
        }
