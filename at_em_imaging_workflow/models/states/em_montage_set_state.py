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


class EMMontageSetState(object):
    ''' Mixin for tracking major changes in the life cycle of an
    :class:`EMMontageSet<at_em_imaging_workflow.models.e_m_montage_set.EMMontageSet>`

    .. figure:: _static/e_m_montage_set_states.png
        :height: 300px
    '''

    class STATE:
        EM_MONTAGE_SET_PENDING = "PENDING"
        '''Initial created state.'''

        EM_MONTAGE_SET_PROCESSING = "PROCESSING"
        '''Indicates the data is progressing through the workflow'''

        EM_MONTAGE_SET_QC = "MONTAGE_QC"
        '''The data is undergoing automated and manual quality control'''

        EM_MONTAGE_SET_REIMAGE = "REIMAGE"
        '''Used to mark data to be reimaged.'''

        EM_MONTAGE_SET_QC_FAILED = "MONTAGE_QC_FAILED"
        '''Used to mark failed automatic or manual quality control'''

        EM_MONTAGE_SET_QC_PASSED = "MONTAGE_QC_PASSED"
        '''Used to mark passed automatic or manual quality control'''

        EM_MONTAGE_SET_REDO_POINT_MATCH = "REDO_POINT_MATCH"
        '''Used to trigger a new point match with alternate parameters'''

        EM_MONTAGE_SET_REDO_SOLVER = "REDO_SOLVER"
        '''Used to trigger a new point match solve with alternate parameters'''

        EM_MONTAGE_SET_FAILED = "FAILED"
        '''Used to indicate a temporary or permanent failure condition.'''

        EM_MONTAGE_SET_GAP = "GAP"
        '''Used to exclude the montage set from rough alignment.'''

        EM_MONTAGE_SET_REPAIR = "REPAIR"
        '''Indicate an exceptional state that may be salvaged offline.'''

        EM_MONTAGE_SET_NOT_SELECTED = "REIMAGED_NOT_SELECTED"
        '''Indicate a reimaged montage set that did not improved quality.'''

    @transition(
        field='object_state',
        source=[
            STATE.EM_MONTAGE_SET_PENDING,
            STATE.EM_MONTAGE_SET_PROCESSING
        ],
        target=STATE.EM_MONTAGE_SET_PROCESSING)
    def start_processing(self):
        '''Processing may begin from the pending state, allow setting twice.'''
        pass

    @transition(
        field='object_state',
        source=[
            STATE.EM_MONTAGE_SET_PROCESSING
        ],
        target=STATE.EM_MONTAGE_SET_PENDING)
    def reset_pending(self):
        '''The processing state may be reset to pending.'''
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
        '''Quality control comes after processing or redoing point match or solver.'''
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
