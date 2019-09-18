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
from django_fsm import transition


class ReferenceSetState(object):
    ''' Mixin for tracking major changes in the life cycle of a
    :class:`ReferenceSet<at_em_imaging_workflow.models.reference_set.ReferenceSet>`
    (representing a :term:`lens correction`).

    .. figure:: _static/reference_set_states.png
        :height: 300px
    '''

    class STATE:
        LENS_CORRECTION_PENDING = "PENDING"
        '''Initial created state.'''

        LENS_CORRECTION_PROCESSING = "PROCESSING"
        '''Indicates the data is progressing through the workflow'''

        LENS_CORRECTION_DONE = "DONE"
        '''Assigned montage sets may be processed'''

        LENS_CORRECTION_REDO = "REDO_LENS_CORRECTION"
        '''Request reprocessing with alternate parameters
        stored in a configuration object
        '''

        LENS_CORRECTION_FAILED = "FAILED"
        '''Processing could not be completed successfully.
        It may be redone with an alternate configuration
        or associated montage sets should be reassigned.
        '''

    @transition(
        field='object_state',
        source='*',
        target=STATE.LENS_CORRECTION_PENDING)
    def reset_pending(self):
        '''Any state may be reset to pending. Should only be used for manual operations.'''
        pass

    @transition(
        field='object_state',
        source=STATE.LENS_CORRECTION_PENDING,
        target=STATE.LENS_CORRECTION_PROCESSING)
    def start_processing(self):
        '''Processing may only begin from the pending state.'''
        pass

    @transition(
        field='object_state',
        source=STATE.LENS_CORRECTION_PROCESSING,
        target=STATE.LENS_CORRECTION_DONE)
    def finish_processing(self):
        '''The done state must be reached through processing.'''
        pass

    @transition(
        field='object_state',
        source='*',
        target=STATE.LENS_CORRECTION_FAILED)
    def fail(self):
        '''The failed state can be set from any other state.'''
        pass

    @transition(
        field='object_state',
        source=[
            STATE.LENS_CORRECTION_PENDING,
            STATE.LENS_CORRECTION_FAILED
        ],
        target=STATE.LENS_CORRECTION_REDO)
    def redo(self):
        '''Processing with alternate parameters may be triggered from a failed state,
        or from pending (i.e. for a series of reference sets expected to need similar treatment)'''
        pass
