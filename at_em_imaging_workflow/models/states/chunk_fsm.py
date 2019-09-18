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
from django_fsm import transition

class ChunkFsm(object):
    ''' Mixin for tracking major changes in the life cycle of a
    :class:`Chunk<at_em_imaging_workflow.models.chunk.Chunk>`
    Generally this is related to :term:`rough alignment`,
    :term:`fine alignment`, :term:`fusion` and :term:`upload`

    .. figure:: _static/load_states.png
        :height: 300px
    '''

    class STATE:
        CHUNK_INCOMPLETE = "PENDING"
        '''Initial created state.'''

        CHUNK_PROCESSING = "PROCESSING"
        '''Indicates the data is progressing through the workflow'''

        CHUNK_ROUGH_QC = "ROUGH_QC"
        '''The data is undergoing automated and manual quality control'''

        CHUNK_ROUGH_QC_FAILED = "ROUGH_QC_FAILED"
        '''Used to mark failed automatic or manual quality control'''

        CHUNK_ROUGH_QC_PASSED = "ROUGH_QC_PASSED"
        '''Used to mark passed automatic or manual quality control'''

        CHUNK_POINT_MATCH_QC_FAILED = "POINT_MATCH_QC_FAILED"
        '''Used to mark failed automatic or manual quality control'''

        CHUNK_POINT_MATCH_QC_PASSED = "POINT_MATCH_QC_PASSED"
        '''Used to mark passed automatic or manual quality control'''

        CHUNK_FINE_QC_FAILED = "FINE_QC_FAILED"
        '''Used to mark failed automatic or manual quality control'''

        CHUNK_FINE_QC_PASSED = "FINE_QC_PASSED"
        '''Used to mark passed automatic or manual quality control'''

        CHUNK_PENDING_FUSION = "PENDING_FUSION"
        '''Used to indicate a chunk should remain in a wait state prior to fusion'''

        CHUNK_FUSING = "FUSING"
        '''Indicates the chunk is progressing through the fusion workflow'''

        CHUNK_FUSION_QC = "FUSION_QC"
        '''The data is undergoing automated and quality control after fusion'''

        CHUNK_FUSION_QC_FAILED = "FUSION_QC_FAILED"
        '''Used to mark failed automatic or manual quality control after fusion'''

        CHUNK_FUSION_QC_PASSED = "FUSION_QC_PASSED"
        '''Used to mark passed automatic or manual quality control after fusion'''

        CHUNK_PENDING_RENDER = "PENDING_RENDER"
    
        CHUNK_NOT_VALID = "NOT_VALID"
    '''Indicates the chunk will no longer be used'''

    @transition(
        field='object_state',
        source=STATE.CHUNK_INCOMPLETE,
        target=STATE.CHUNK_PROCESSING)
    def start_processing(self):
        '''Processing may begin, set when all montage sets are ready.'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_PROCESSING,
        target=STATE.CHUNK_INCOMPLETE)
    def reset_incomplete(self):
        '''The processing state may be reset to pending (i.e. if the z range is extended).'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_PROCESSING,
        target=STATE.CHUNK_ROUGH_QC)
    def finish_processing(self):
        '''Quality control comes after rough alignment.'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_ROUGH_QC,
        target=STATE.CHUNK_PROCESSING)
    def redo_processing(self):
        '''Rough alignment for a chunk may be restarted if individual montage sets change.'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_ROUGH_QC,
        target=STATE.CHUNK_ROUGH_QC_FAILED)
    def rough_qc_fail(self):
        '''Used to fail a chunk that is undergoing quality control after rough alignment'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_ROUGH_QC,
        target=STATE.CHUNK_ROUGH_QC_PASSED)
    def rough_qc_pass(self):
        '''Used to pass a chunk that is undergoing quality control after rough alignment'''
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
        '''Used to pass a chunk that is undergoing quality control after point matching'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_POINT_MATCH_QC_PASSED,
        target=STATE.CHUNK_PENDING_FUSION)
    def pending_fusion(self):
        '''Used to indicate a chunk is waiting to be able to begin fusion'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_PENDING_FUSION,
        target=STATE.CHUNK_FUSING)
    def start_fusion(self):
        '''Used to indicate a chunk has started the fusion workflow'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_FUSING,
        target=STATE.CHUNK_FUSION_QC)
    def stop_fusion(self):
        '''Used to indicate a chunk has been fused and is waiting for quality control'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_FUSION_QC,
        target=STATE.CHUNK_FUSION_QC_FAILED)
    def fusion_qc_fail(self):
        '''Used to fail a chunk that is undergoing quality control after fusion'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_FUSION_QC,
        target=STATE.CHUNK_FUSION_QC_PASSED)
    def fusion_qc_pass(self):
        '''Used to pass a chunk that is undergoing quality control after fusion'''
        pass

    @transition(
        field='object_state',
        source=STATE.CHUNK_FUSION_QC_PASSED,
        target=STATE.CHUNK_PENDING_RENDER)
    def pending_render(self):
        pass
