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
from django.db import models
from django.conf import settings
from .rendered_volume import RenderedVolume
import logging

class Chunk(models.Model):
    _log = logging.getLogger('at_em_imaging_workflow.models.chunk')
    size = models.IntegerField(null=True)
    chunk_state = models.CharField(max_length=255, null=True)
    rendered_volume = models.ForeignKey(RenderedVolume)
    preceding_chunk = \
        models.ForeignKey('self',
        related_name='%(class)s_preceding_chunk')
    following_chunk = \
        models.ForeignKey('self',
        related_name='%(class)s_following_chunk')

    def __str__(self):
        return "Chunk Lorem Ipsum"  # TODO: better string

    def set_chunk_size(self):
        #TODO
        self.size = 0

    def is_complete(self):
        raise Exception('unimplimented')
        return True

    @classmethod
    def chunks_for_z_index(cls, z):
        ''' returns one or more chunks that would contain a z-index
        '''
        # TODO: move to class config
        chunk_defaults = settings.CHUNK_DEFAULTS
        size = chunk_defaults['chunk_size']
        overlap = chunk_defaults['overlap']
        size_minus_overlap = size - overlap 
        offset = chunk_defaults['start_z']
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
    def z_indices_for_chunk(cls, c):
        chunk_defaults = settings.CHUNK_DEFAULTS
        start = (
            c * chunk_defaults['chunk_size']
            + chunk_defaults['start_z'])
        stop = start + chunk_defaults['chunk_size']

        return list(range(start, stop))
