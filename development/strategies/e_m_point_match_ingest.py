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
from workflow_engine.strategies.ingest_strategy import IngestStrategy
from django.core.exceptions import ObjectDoesNotExist
from development.models.study import Study
from development.models.specimen import Specimen
from development.models.section import Section
from development.models.load import Load
from development.models.sample_holder import SampleHolder
from development.models.reference_set import ReferenceSet
from development.models.e_m_montage_set import EMMontageSet
from rendermodules.ingest.schemas import \
    example, EMMontageSetIngestSchema
import os
import logging
import traceback

class EMPointMatchIngest(IngestStrategy):
    _log = logging.getLogger('development.strategies.e_m_point_match_ingest')

    def get_workflow_name(self):
        EMPointMatchIngest._log.info('get_workflow_name')

        return 'em_2d_montage_point_match'

    def create_enqueued_object(self, message):
        EMPointMatchIngest._log.info('create_enqueued_object')
        EMPointMatchIngest._log.warn('unimplemented')

        EMPointMatchIngest._log.info('creating study')
        study, _ = Study.objects.update_or_create(
            name='DEADBEEF'
        )

        EMPointMatchIngest._log.info('creating specimen')
        specimen, _ = Specimen.objects.update_or_create(
            uid=message['section']['specimen'],
            defaults={
                'render_project': 'PROJECT Lorem Impsum',
                'render_owner': 'Lorem Imsum',
                'study': study
            })

        EMPointMatchIngest._log.info('creating section')
        section = Section.objects.create(
            z_index=message['section']['z_index'],
            metadata=None,
            specimen=specimen 
        )

        EMPointMatchIngest._log.info('creating load')
        load, _ = Load.objects.update_or_create(
            uid='DEADBEEF'
        )

        EMPointMatchIngest._log.info('creating sample holder')
        sample_holder, _ = SampleHolder.objects.update_or_create(
            uid=message['section']['sample_holder'],
            defaults={
                'imaged_sections_count': 0,
                'load': load
            })

        EMPointMatchIngest._log.info('creating em montage set')

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
        EMPointMatchIngest._log.info(str(em_montage_set))

        return em_montage_set

    def generate_response(self, enqueued_object):
        EMPointMatchIngest._log.info('generate_response')


