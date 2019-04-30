# Allen Institute Software License - This software license is the 2-clause BSD
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
from django_fsm import transition
from workflow_engine.mixins import (
    Enqueueable,
    Configurable,
    HasWellKnownFiles,
    Stateful
)
import itertools as it
import logging


class Chunk(
    Configurable,
    Enqueueable,
    HasWellKnownFiles,
    Stateful,
    models.Model
):
    class Meta:
        db_table = 'development_chunk'

    class STATE:
        CHUNK_INCOMPLETE = "INCOMPLETE"
        CHUNK_PROCESSING = "PROCESSING"
        CHUNK_ROUGH_QC = "ROUGH_QC"
        CHUNK_ROUGH_QC_FAILED = "ROUGH_QC_FAILED"
        CHUNK_ROUGH_QC_PASSED = "ROUGH_QC_PASSED"
        CHUNK_POINT_MATCH_QC_FAILED = "POINT_MATCH_QC_FAILED"
        CHUNK_POINT_MATCH_QC_PASSED = "POINT_MATCH_QC_PASSED"
        CHUNK_FINE_QC_FAILED = "FINE_QC_FAILED"
        CHUNK_FINE_QC_PASSED = "FINE_QC_PASSED"
        CHUNK_PENDING_FUSION = "PENDING_FUSION"
        CHUNK_FUSING = "FUSING"
        CHUNK_FUSION_QC = "FUSION_QC"
        CHUNK_FUSION_QC_FAILED = "FUSION_QC_FAILED"
        CHUNK_FUSION_QC_PASSED = "FUSION_QC_PASSED"
        CHUNK_PENDING_RENDER = "PENDING_RENDER"
        CHUNK_NOT_VALID = "NOT_VALID"

    _log = logging.getLogger('at_em_imaging_workflow.models.chunk')
    size = models.IntegerField(null=True)
    computed_index = models.IntegerField(null=True)
    chunk_state = models.CharField(max_length=255, null=True)
    rendered_volume = models.ForeignKey('RenderedVolume')
    load = models.ForeignKey('Load',null=True, blank=True)
    preceding_chunk = models.ForeignKey(
        'self',
        related_name='%(class)s_preceding_chunk',
        null=True,
        blank=True
    )
    following_chunk = models.ForeignKey(
        'self',
        related_name='%(class)s_following_chunk',
        null=True,
        blank=True
    )

    def __str__(self):
        return 'chunk {} {}'.format(self.computed_index, self.id)

    def set_chunk_size(self):
        #TODO
        self.size = 0

    def is_complete(self):
        return len(self.missing_sections()) == 0

    # TODO: move this to render project manager
    def get_render_project_name(self):
        # return '247488_8R'
        return self.sections.first().specimen.uid

    def dimensions(self):
        camera = self.sections.first().montageset_set.first().camera

        return (camera.height, camera.width)

    def get_point_collection_name(self):
        return 'chunk_rough_align_point_matches'
        #return '17797_1R_rough_point_matches'

    def tile_pairs_file_description(self):
        return 'rough tile pairs file'

    @classmethod
    def assign_to_chunks(cls, em_mset, remove_others=False):
        if remove_others:
            raise Exception('unimplemented')

        z_index = em_mset.get_section_z_index()

        load_object = em_mset.get_load()
        load_chunks = load_object.chunk_set.all()

        chunks_to_assign = []

        for c in load_chunks:
            z_mapping = c.get_z_mapping()

            if str(z_index) in z_mapping:
                chunks_to_assign.append(c)

        for c in chunks_to_assign:
            ChunkAssignment.objects.update_or_create(
                chunk=c,
                section=em_mset.section
            )

        return chunks_to_assign

    def get_z_mapping(self):
        return self.configurations.get(
            configuration_type='z_mapping'
        ).json_object

    @classmethod
    def get_montage_set_for_rough_alignment(cls, section):
        return section.montageset_set.get()

    def missing_sections(self):
        z_mapping = self.get_z_mapping()
        mapping_zs = set(int(z) for z in z_mapping.keys())

        section_zs = set(
            m.section.z_index for m in it.chain.from_iterable(
                s.montageset_set.filter(
                    object_state__in=[
                        'GAP',
                        'REIMAGE',
                        'MONTAGE_QC_PASSED'
                       # EMMontageSet.STATE.EM_MONTAGE_SET_GAP,
                        #EMMontageSet.STATE.EM_MONTAGE_SET_REIMAGE,
                        #EMMontageSet.STATE.EM_MONTAGE_SET_QC_PASSED
                    ]
                ) for s in self.sections.all()
            )
        )

        return mapping_zs - section_zs

    def get_tile_pair_ranges(self):
        tile_pair_config= self.configurations.get(
            configuration_type='chunk_configuration'
        ).json_object

        return tile_pair_config['tile_pair_ranges']

    def z_info(self):
        z_mapping = self.get_z_mapping()
        tile_pair_ranges = self.get_tile_pair_ranges()
        min_z, max_z = self.calculate_z_min_max(tile_pair_ranges)

        return z_mapping, min_z, max_z

    def calculate_z_min_max(self, tile_pair_ranges):
        min_z = min([rng['minz'] for rng in tile_pair_ranges.values()])
        max_z = max([rng['maxz'] for rng in tile_pair_ranges.values()])

        return min_z,max_z

    def storage_basename(self):
        _, z_start,z_end = self.z_info()

        return '{}_zs{}_ze{}'.format(
            self.computed_index,
            str(z_start),
            str(z_end)
        )

    @transition(
        field='object_state',
        source=STATE.CHUNK_INCOMPLETE,
        target=STATE.CHUNK_PROCESSING)
    def start_processing(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_PROCESSING,
        target=STATE.CHUNK_INCOMPLETE)
    def reset_incomplete(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_PROCESSING,
        target=STATE.CHUNK_ROUGH_QC)
    def finish_processing(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_ROUGH_QC,
        target=STATE.CHUNK_PROCESSING)
    def redo_processing(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_ROUGH_QC,
        target=STATE.CHUNK_ROUGH_QC_FAILED)
    def rough_qc_fail(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_ROUGH_QC,
        target=STATE.CHUNK_ROUGH_QC_PASSED)
    def rough_qc_pass(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_ROUGH_QC_PASSED,
        target=STATE.CHUNK_POINT_MATCH_QC_FAILED)
    def point_match_fail(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_ROUGH_QC_PASSED,
        target=STATE.CHUNK_POINT_MATCH_QC_PASSED)
    def point_match_pass(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_POINT_MATCH_QC_PASSED,
        target=STATE.CHUNK_PENDING_FUSION)
    def pending_fusion(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_PENDING_FUSION,
        target=STATE.CHUNK_FUSING)
    def start_fusion(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_FUSING,
        target=STATE.CHUNK_FUSION_QC)
    def stop_fusion(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_FUSION_QC,
        target=STATE.CHUNK_FUSION_QC_FAILED)
    def fusion_qc_fail(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_FUSION_QC,
        target=STATE.CHUNK_FUSION_QC_PASSED)
    def fusion_qc_pass(self):
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_FUSION_QC_PASSED,
        target=STATE.CHUNK_PENDING_RENDER)
    def pending_render(self):
        pass

# circular imports
from at_em_imaging_workflow.models import (
    ChunkAssignment
)
