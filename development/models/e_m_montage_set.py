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
from development.models.montage_set import MontageSet
from development.models.reference_set import ReferenceSet
import os


class EMMontageSet(MontageSet):
    reference_set = models.ForeignKey(ReferenceSet, null=True)
    reference_set_uid = models.CharField(max_length=255, null=True)

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

    def specimen(self):
        return self.section.specimen

    def z_index(self):
        return self.section.z_index

    specimen.admin_order_field = 'section__specimen__uid'
    z_index.admin_order_field = 'section__z_index'

    def tile_pairs_file_description(self):
        return 'tile pairs file'

    def get_point_collection_name(self):
        return 'default_point_matches'

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

