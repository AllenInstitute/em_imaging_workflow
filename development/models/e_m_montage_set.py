# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2017-2018. Allen Institute. All rights reserved.
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
from django.db import models
from django.conf import settings
from django_fsm import transition
from django.core.exceptions import ObjectDoesNotExist
from development.models import MontageSet
import os


class EMMontageSet(MontageSet):
    class STATE:
        EM_MONTAGE_SET_PENDING = "PENDING"
        EM_MONTAGE_SET_PROCESSING = "PROCESSING"
        EM_MONTAGE_SET_QC = "MONTAGE_QC"
        EM_MONTAGE_SET_REIMAGE = "REIMAGE"
        EM_MONTAGE_SET_QC_FAILED = "MONTAGE_QC_FAILED"
        EM_MONTAGE_SET_QC_PASSED = "MONTAGE_QC_PASSED"
        EM_MONTAGE_SET_REDO_POINT_MATCH = "REDO_POINT_MATCH"
        EM_MONTAGE_SET_REDO_SOLVER = "REDO_SOLVER"
        EM_MONTAGE_SET_FAILED = "FAILED"
        EM_MONTAGE_SET_GAP = "GAP"
        EM_MONTAGE_SET_REPAIR = "REPAIR"
        EM_MONTAGE_SET_NOT_SELECTED = "REIMAGED_NOT_SELECTED"

    reference_set = models.ForeignKey('ReferenceSet',
                                      null=True, blank=True)
    reference_set_uid = models.CharField(max_length=255,
                                         null=True, blank=True)

    def __str__(self):
        try:
            specimen_id = self.section.specimen.uid
        except:
            specimen_id = 'X'

        try:
            z_index = str(self.section.z_index)
        except:
            z_index = 'X'

        return "%s_%s_%s" % (
            specimen_id,
            z_index,
            str(self.acquisition_date))

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_PENDING,
        target=STATE.EM_MONTAGE_SET_PROCESSING)
    def start_processing(self):
        pass

    @transition(
        field='object_state',
        source=[
            STATE.EM_MONTAGE_SET_PROCESSING,
            STATE.EM_MONTAGE_SET_REDO_POINT_MATCH,
            STATE.EM_MONTAGE_SET_REDO_SOLVER
        ],
        target=STATE.EM_MONTAGE_SET_QC)
    def finish_processing(self):
        pass

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_REDO_POINT_MATCH,
        target=STATE.EM_MONTAGE_SET_QC)
    def finish_redo_point_match(self):
        pass

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_REDO_SOLVER,
        target=STATE.EM_MONTAGE_SET_QC)
    def finish_redo_solver(self):
        pass

    @transition(
        field='object_state',
        source=[
            STATE.EM_MONTAGE_SET_QC,
            STATE.EM_MONTAGE_SET_REDO_POINT_MATCH,
            STATE.EM_MONTAGE_SET_REDO_SOLVER,
            STATE.EM_MONTAGE_SET_QC_FAILED,
            STATE.EM_MONTAGE_SET_PENDING,
            STATE.EM_MONTAGE_SET_PROCESSING,
            STATE.EM_MONTAGE_SET_QC_PASSED
        ],
        target=STATE.EM_MONTAGE_SET_QC_PASSED)
    def pass_qc(self):
        pass

    @transition(
        field='object_state',
        source=[
            STATE.EM_MONTAGE_SET_QC,
            STATE.EM_MONTAGE_SET_QC_PASSED,
            STATE.EM_MONTAGE_SET_QC_FAILED,
            STATE.EM_MONTAGE_SET_REDO_POINT_MATCH,
            STATE.EM_MONTAGE_SET_REDO_SOLVER,
            STATE.EM_MONTAGE_SET_PENDING,
        ],
        target=STATE.EM_MONTAGE_SET_QC_FAILED)
    def fail_qc(self):
        pass

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_QC_FAILED,
        target=STATE.EM_MONTAGE_SET_REDO_POINT_MATCH)
    def redo_point_match(self):
        pass

    @transition(
        field='object_state',
        source='*',
        target=STATE.EM_MONTAGE_SET_PROCESSING)
    def redo_processing(self):
        pass

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_QC_FAILED,
        target=STATE.EM_MONTAGE_SET_REDO_SOLVER)
    def redo_solver(self):
        pass

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_QC_FAILED,
        target=STATE.EM_MONTAGE_SET_REIMAGE)
    def reimage(self):
        pass

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_QC_FAILED,
        target=STATE.EM_MONTAGE_SET_FAILED)
    def fail(self):
        pass

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_QC_FAILED,
        target=STATE.EM_MONTAGE_SET_NOT_SELECTED)
    def reimage_not_select(self):
        pass

    @transition(
        field='object_state',
        source=STATE.EM_MONTAGE_SET_QC_FAILED,
        target=STATE.EM_MONTAGE_SET_GAP)
    def gap(self):
        pass

    def specimen(self):
        return self.section.specimen

    def z_index(self):
        return self.section.z_index

    specimen.admin_order_field = 'section__specimen__uid'
    z_index.admin_order_field = 'section__z_index'

    def tile_pairs_file_description(self):
        return 'tile pairs file'

    def get_point_collection_name(self):
        reimage_index = self.reimage_index()

        if reimage_index:
            reimage_suffix = '_reimage_{}'.format(reimage_index)
        else:
            reimage_suffix = ''

        return 'default_point_matches{}'.format(reimage_suffix)

    def get_render_project_name(self):
        return self.section.specimen.uid

    def get_storage_directory(self, base_storage_directory=None):
        if base_storage_directory is None:
            base_storage_directory = settings.BASE_FILE_PATH

        section = self.section
        specimen = section.specimen

        return os.path.join(base_storage_directory,
                            'em_montage_' + \
                            specimen.uid + '_z' + \
                            str(section.z_index) + '_' + \
                            self.clean_acquisition_date())

    def reimage_index(self):
        try:
            cfg = self.configurations.get(
                configuration_type='rough_align_parameters'
            )
            reimage_idx = cfg.json_object['reimage_index']
        except:
            unique_section = self.section
    
            em_msets = [
                mset.emmontageset 
                for mset
                in unique_section.montageset_set.order_by('id')
            ]
    
            em_mset_ids = [em_mset.id for em_mset in em_msets]
            reimage_idx = em_mset_ids.index(self.id)

        return reimage_idx

    def reimage_count(self):
        return self.section.montageset_set.count()

    def get_em_2d_solver_lambda(self, default_lbda):
        cfg,_ = self.configurations.get_or_create(
            configuration_type='point_match_parameters',
            defaults= {
                'name': 'point match params for montage set {}'.format(
                    self.id),
                'json_object': { 'default_lambda': default_lbda }
            })

        if 'default_lambda' not in cfg.json_object:
            cfg.json_object['default_lambda'] = default_lbda
            cfg.save()

        return cfg.json_object['default_lambda']

    def get_redo_parameters(self):
        #cfg = {
        #    'default_lambda': 5.0,
        #    'render_scale': 0.4,
        #    'transformation': 'Polynomial2DTransform',
        #    'poly_order': 2
        #}
        cfg = {
           'default_lambda': None,
           'render_scale': None,
           'transformation': None, 
           'poly_order': None
        }

        # if self.microscope.uid == 'temca3':
        #     cfg['transformation'] = None
        #     cfg['poly_order'] = None

        reimage_index = self.reimage_index()
        if reimage_index > 0:
            suffix = ' reimage {}'.format(reimage_index)
        else:
            suffix = ''

        # params,_ = self.configurations.get_or_create(
        #     name='point match params for {}{}'.format(
        #         str(self),
        #         suffix),
        #     configuration_type='point_match_parameters',
        #     defaults={
        #         'json_object': cfg
        #     })

        try:
          params = self.configurations.get(
              configuration_type='point_match_parameters')
          return params.json_object
        except:
            return cfg

    def update_point_match_state(self, point_match_state):
        reimage_index = self.reimage_index()
        if reimage_index > 0:
            suffix = ' reimage {}'.format(reimage_index)
        else:
            suffix = ""

        try:
            config = self.configurations.get(
                configuration_type='point_match_parameters')
            config.json_object.update(point_match_state)
            config.save()
        except ObjectDoesNotExist:
            self.configurations.create(
                name='point match params for {}{}'.format(
                    str(self),
                    suffix),
                configuration_type='point_match_parameters',
                json_object=point_match_state)
