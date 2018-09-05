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
from django_fsm import transition
from development.models.tile_image_set import TileImageSet
import os


class ReferenceSet(TileImageSet):
    class STATE:
        LENS_CORRECTION_PENDING = "PENDING"
        LENS_CORRECTION_PROCESSING = "PROCESSING"
        LENS_CORRECTION_DONE = "DONE"
        LENS_CORRECTION_REDO = "REDO_LENS_CORRECTION"
        LENS_CORRECTION_FAILED = "FAILED"

    uid = models.CharField(max_length=255, null=True)
    project_path = models.CharField(max_length=255) # deprecate for storage_dir
    manifest_path = models.CharField(max_length=255, null=True) # well_known_file?

    def __str__(self):
        return str(self.acquisition_date)

    def get_render_project_name(self):
        return "em_2d_montage_staging"

    def get_storage_directory(self, base_storage_directory=None):
        if base_storage_directory is None:
            base_storage_directory = settings.BASE_FILE_PATH
            
        return os.path.join(base_storage_directory,
                            'reference_' + \
                            self.clean_acquisition_date())

    @transition(
        field='object_state',
        source='*',
        target=STATE.LENS_CORRECTION_PENDING)
    def reset_pending(self):
        pass

    @transition(
        field='object_state',
        source=STATE.LENS_CORRECTION_PENDING,
        target=STATE.LENS_CORRECTION_PROCESSING)
    def start_processing(self):
        pass

    @transition(
        field='object_state',
        source=STATE.LENS_CORRECTION_PROCESSING,
        target=STATE.LENS_CORRECTION_DONE)
    def finish_processing(self):
        pass

    @transition(
        field='object_state',
        source='*',
        target=STATE.LENS_CORRECTION_FAILED)
    def fail(self):
        pass

    @transition(
        field='object_state',
        source=STATE.LENS_CORRECTION_FAILED,
        target=STATE.LENS_CORRECTION_REDO)
    def redo(self):
        pass