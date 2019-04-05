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
from django.conf import settings
from django_fsm import FSMField, transition
from workflow_engine.mixins import (
    Enqueueable,
    Configurable,
    HasWellKnownFiles
)
import logging


class Chunk(Configurable, Enqueueable, HasWellKnownFiles, models.Model):
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
    object_state = FSMField(default=STATE.CHUNK_INCOMPLETE)
    rendered_volume = models.ForeignKey('RenderedVolume')
    preceding_chunk = \
        models.ForeignKey('self',
        related_name='%(class)s_preceding_chunk',
        null=True, blank=True)
    following_chunk = \
        models.ForeignKey('self',
        related_name='%(class)s_following_chunk',
        null=True, blank=True)

    def __str__(self):
        return 'chunk {} {}'.format(self.computed_index, self.id)

    def set_chunk_size(self):
        #TODO
        self.size = 0

    def is_complete(self):
        # raise Exception('unimplimented')
        return True

    def get_render_project_name(self):
        # return '247488_8R'
        return self.sections.first().specimen.uid

    def z_list(self):
        secs = self.sections.all()
        zs = [sec.z_index for sec in secs]

        return zs

    def z_range(self):
        zs = self.z_list()

        return (min(zs), max(zs))

    def dimensions(self):
        camera = self.sections.first().montageset_set.first().camera

        return (camera.height, camera.width)


    def get_point_collection_name(self):
        return 'chunk_rough_align_point_matches'
        #return '17797_1R_rough_point_matches'

    def tile_pairs_file_description(self):
        return 'rough tile pairs file'

    @classmethod
    def get_z_range(cls, em_mset):
        z_index = em_mset.z_index()

    @classmethod
    def chunks_for_z_index(cls, load_offset, z):
        ''' returns one or more chunks that would contain a z-index
        '''
        chunk_defaults = settings.CHUNK_DEFAULTS
        size = chunk_defaults['chunk_size']
        overlap = chunk_defaults['overlap']
        size_minus_overlap = size - overlap 
        offset = load_offset
        z_no_offset = z - offset
        chunk_id = z_no_offset // size_minus_overlap
        z_within_chunk = z_no_offset % size_minus_overlap

        if z_within_chunk < overlap:
            if chunk_id > 0:
                return [ chunk_id - 1, chunk_id ]
            else:
                return [ chunk_id ]
        else:
            return [ chunk_id ]

    @classmethod
    def calculate_z_range(cls, c):
        # TODO: this does not take offset into account
        chunk_defaults = settings.CHUNK_DEFAULTS

        z_start = (
            c * chunk_defaults['chunk_size']
            + chunk_defaults['start_z']
            - c * chunk_defaults['overlap'])

        z_end = z_start + chunk_defaults['chunk_size']

        return (z_start, z_end)

    @classmethod
    def z_indices_for_chunk(cls, c):
        (z_start, z_end) = Chunk.calculate_z_range(c)

        return list(range(z_start, z_end))

    @classmethod
    def assign_montage_set_to_chunks(cls, mset):
        mipmap_directory = '/path/to/mock/mipmaps'
        default_state = 'PENDING'

        volume, _ = RenderedVolume.objects.update_or_create(
            specimen=mset.section.specimen,
            defaults={
                'mipmap_directory': mipmap_directory,
            })

        chunk_index_list = Chunk.chunks_for_z_index(
            mset.sample_holder.load.offset,
            mset.get_section_z_index())
        chunk_list = []

        for c_idx in chunk_index_list:
            c, _ = Chunk.objects.update_or_create(
                computed_index=c_idx,
                defaults={
                    'size': settings.CHUNK_DEFAULTS['chunk_size'],
                    'rendered_volume': volume,
                    'object_state': Chunk.STATE.CHUNK_INCOMPLETE,
                    'following_chunk_id': None,
                    'preceding_chunk_id': None})
            chunk_list.append(c)

        mset_section = mset.section

        for c in chunk_list:
            ChunkAssignment.objects.update_or_create(
                section=mset_section,
                chunk=c)

        return chunk_list

    def get_z_mapping(self):
        return self.configurations.get(
            configuration_type='z_mapping'
        ).json_object

    @classmethod
    def get_montage_set_for_rough_alignment(cls, section):
        return section.montageset_set.get()

    def missing_sections(self):
        z_mapping = self.get_z_mapping()
        sections = self.sections.all()
    
        section_zs = set(
            s.z_index for s in sections 
            if Chunk.get_montage_set_for_rough_alignment(
                s
            ).object_state in [
                'REIMAGE',
                'GAP',
                'MONTAGE_QC_PASSED'
            ]
        )
        mapping_zs = set(int(z) for z in z_mapping.keys())
    
        return mapping_zs - section_zs

    def get_tile_pair_ranges(self):
        tile_pair_config= self.configurations.get(
            configuration_type='chunk_configuration'
        ).json_object

        return tile_pair_config['tile_pair_ranges']

    def calculate_z_min_max(self, tile_pair_ranges):
        min_z = min([rng['minz'] for rng in tile_pair_ranges.values()])
        max_z = max([rng['maxz'] for rng in tile_pair_ranges.values()])

        return min_z,max_z

    def storage_basename(self):
        tile_pair_ranges = self.get_tile_pair_ranges()
        z_start,z_end = self.calculate_z_min_max(tile_pair_ranges)

        return '{}_zs{}_ze{}'.format(
            self.computed_index,
            str(z_start),
            str(z_end)
        )

    def get_load(self):
        try:
            load_object = self.sections.first(
                ).montageset_set.first(
                    ).sample_holder.load
        except:
            load_object = None

        return load_object

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
from development.models.rendered_volume import RenderedVolume
from development.models.chunk_assignment import ChunkAssignment
