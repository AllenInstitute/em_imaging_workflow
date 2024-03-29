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
from django.conf import settings
from workflow_engine.mixins import (
    Configurable,
    Enqueueable,
    HasWellKnownFiles,
    Stateful
)
from django.db import models
from pytz import timezone
import re


class TileImageSet(
    Configurable,
    Enqueueable,
    HasWellKnownFiles,
    Stateful,
    models.Model
):
    storage_directory = models.CharField(max_length=500, null=True)
    camera = models.ForeignKey(
        'Camera',
        null=True,
        on_delete=models.CASCADE
    )
    microscope = models.ForeignKey(
        'Microscope',
        null=True,
        on_delete=models.CASCADE
    )
    metafile = models.CharField(max_length=500, null=True)
    acquisition_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'development_tileimageset'

    _ODD_FILE_CHARS = re.compile(r'[ :\.\-\+]')

    def __str__(self):
        return str(self.acquisition_date)

    def local_acquisition_date_str(self):
        TZ = timezone(settings.TIME_ZONE)
        local_acquisition_date = TZ.fromutc(
            self.acquisition_date.replace(tzinfo=None))

        return str(local_acquisition_date)

    def clean_acquisition_date(self):
        return re.sub(TileImageSet._ODD_FILE_CHARS,
                      '_',
                      str(self.acquisition_date))
