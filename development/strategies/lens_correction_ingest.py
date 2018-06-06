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
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from workflow_engine.strategies.ingest_strategy import IngestStrategy
from development.models.camera import Camera
from development.models.microscope_type import MicroscopeType 
from development.models.microscope import Microscope
from development.models.reference_set import ReferenceSet
from development.models.study import Study
from development.models.specimen import Specimen
from development.models.section import Section
from development.models.sample_holder import SampleHolder
from development.models.load import Load
from development.models.e_m_montage_set import EMMontageSet
from development.models import state_machines
import logging
import uuid

class LensCorrectionIngest(IngestStrategy):
    _log = logging.getLogger('development.strategies.lens_correction_ingest')

    # TODO, query from datbase using class name
    def get_workflow_name(self):
        LensCorrectionIngest._log.info('get_workflow_name')

        return 'em_2d_montage'

    def create_camera(self, message_camera):
        '''Add or retrieve and optionally modify a Camera in the database.
        
        Parameters
        ----------
        message_camera : dict
            height, width, model keys
        
        Returns
        -------
        Camera
            the database object
        '''
        camera, _ = \
            Camera.objects.update_or_create(
                uid=message_camera['camera_id'],
                defaults={
                    'height': message_camera['height'],
                    'width': message_camera['width'],
                    'model': message_camera['model']})

        return camera

    def create_microscope(self,
                          message_microscope,
                          message_microscope_type):
        '''Add or retrieve and optionally modify a Microscope
        in the database.

        Parameters
        ----------
        message_microscope : dict
            the sub-message to be unpacked

        Returns
        -------
        Microscope
            the database object
        '''
        scope_type, _ = \
            MicroscopeType.objects.update_or_create(
                name=message_microscope_type)

        microscope, _ = \
            Microscope.objects.update_or_create(
                uid=message_microscope,
                defaults={
                    'microscope_type': scope_type
                })

        return microscope

    def create_reference_set(self, message):
        '''Add or retrieve and optionally modify a Microscope
        in the database. Camera and Microscope are created if needed.

        Parameters
        ----------
        message_microscope : dict
            the sub-message to be unpacked

        Returns
        -------
        ReferenceSet
            the database object
        '''
        LensCorrectionIngest._log.info('create_enqueued_object')

        camera = self.create_camera(
            message['acquisition_data']['camera'])
        microscope = self.create_microscope(
            message['acquisition_data']['microscope'],
            message['acquisition_data']['microscope_type'])

        metafile = message['metafile']
        manifest_path = message['manifest_path']

        reference_set, _ = ReferenceSet.objects.update_or_create(
                uid=uuid.uuid4(),
                defaults= {
                    'storage_directory': message['storage_directory'],
                    'metafile': metafile,
                    'workflow_state': state_machines.states(
                        ReferenceSet).PENDING,
                    'camera': camera,
                    'microscope': microscope,
                    'acquisition_date':
                        message['acquisition_data']['acquisition_time'],
                    # 'project_path': '/example_data', # deprecated
                    'manifest_path': manifest_path,
                    'metafile': metafile
                })

        return reference_set

    def create_study(self, study_message):
        LensCorrectionIngest._log.warn('creating study - UNIMPLEMENTED')

        study, _ = Study.objects.update_or_create(
            name='IARPA Phase 2' # TODO: from settings or ingest
        )

        return study

    def create_specimen(self, specimen_message, study):
        LensCorrectionIngest._log.info('creating specimen')
        specimen, _ = Specimen.objects.update_or_create(
            uid=specimen_message,
            defaults={
                'render_project': settings.RENDER_SERVICE_PROJECT,
                'render_owner': settings.RENDER_SERVICE_USER,
                'study': study
            })

        return specimen

    def create_section(self, section_message, metafile, specimen):
        LensCorrectionIngest._log.info('creating section')

        section, _ = Section.objects.update_or_create(
            z_index=section_message['z_index'],
            specimen=specimen,
            defaults={
                'metadata': None
            })

        return section

    # TODO: ask RobY, Russel doesn't know what a load is.
    def create_load(self, load_message):
        LensCorrectionIngest._log.warn('creating load - UNIMPLEMENTED')

        load, _ = Load.objects.update_or_create(
            uid='Load'
        )

        return load

    def create_sample_holder(self, sample_holder_message, load):
        LensCorrectionIngest._log.info('creating sample holder')

        sample_holder, _ = SampleHolder.objects.update_or_create(
            uid=sample_holder_message,
            defaults={
                'imaged_sections_count': 0,
                'load': load
            })

        return sample_holder

    def create_enqueued_object(self, message, tags=None):
        if tags == None:
            tags = ['EMMontageSet']

        if 'ReferenceSet' in tags:
            enqueued_object = self.create_reference_set(message)
            start_node = 'Generate Lens Correction Transform'
        elif 'EMMontageSet' in tags:
            enqueued_object = self.create_em_montage_set(message)
            start_node = 'Generate Render Stack'
        else:
            LensCorrectionIngest._log.warn("No enqueued object type tag")
            enqueued_object = None
            start_node = 'Generate Render Stack'

        return enqueued_object, start_node

    def create_em_montage_set(self, message):
        LensCorrectionIngest._log.info('create_em_montage_set')

        study = self.create_study(message)
        specimen = self.create_specimen(
            message['section']['specimen'],
            study)
        section = self.create_section(message['section'],
                                      message['metafile'],
                                      specimen)
        load = self.create_load(None)
        sample_holder = self.create_sample_holder(
            message['section']['sample_holder'],
            load)

        camera = self.create_camera(
            message['acquisition_data']['camera'])
        microscope = self.create_microscope(
            message['acquisition_data']['microscope'],
            message['acquisition_data']['microscope_type'])

        LensCorrectionIngest._log.info('creating em montage set')

        # if reference set id isn't specified,
        # montage set should still be created
        reference_set = None
        reference_set_uid = None

        # TODO fix this logic and raise real exception
        if 'reference_set_id' in message:
            reference_set_uid = message['reference_set_id']
            try:
                reference_set = ReferenceSet.objects.get(
                    uid=reference_set_uid)
            except ObjectDoesNotExist:
                pass

        em_montage_set = EMMontageSet.objects.create(
            uid=uuid.uuid4(),
            acquisition_date=message['acquisition_data']['acquisition_time'],
            overlap=message['acquisition_data']['overlap'],
            workflow_state=state_machines.states(ReferenceSet).PENDING,
            mipmap_directory=None,
            section=section,
            sample_holder=sample_holder,
            reference_set=reference_set,
            reference_set_uid=reference_set_uid,
            storage_directory=message['storage_directory'],
            metafile=message['metafile'],
            camera=camera,
            microscope=microscope)
        LensCorrectionIngest._log.info(str(em_montage_set))

        return em_montage_set

    def generate_response(self, enqueued_object):
        LensCorrectionIngest._log.info('generate_response')

        return {
            'enqueued_object_uid': enqueued_object.uid
        }
