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
from workflow_engine.mixins import Configurable, Enqueueable, Stateful
from .states import LoadState
import pandas as pd
import copy


class Load(
    Configurable,
    Enqueueable,
    Stateful,
    LoadState,
    models.Model):

    uid = models.CharField(max_length=255, null=True)
    offset = models.IntegerField(null=True)

    class Meta:
        db_table = 'development_load'

    def __str__(self):
        return str(self.uid)

    def read_mapping_spreadsheet(self, mapping_xls_filename, sheet=None):
        if sheet is None:
            sheet = self.uid

        xls_df = pd.read_excel(
            mapping_xls_filename, sheet_name=self.uid)

        return xls_df

    def get_z_mapping(self):
        return copy.deepcopy(
            self.configurations.get(
                configuration_type='z_mapping').json_object)

    def calculate_offset_z_range(self, z_range):
        '''Apply the microscope Load (tapes) fixed integer offset to the min and max z's.

        Parameters
        ----------
        z_range : tuple of two ints
            min z, max z in tape coordinates
        
        Returns
        -------
        tuple of two integers
            min z, max z in temp coordinates
        '''
        return (z_range[0] + self.offset, z_range[1] + self.offset)

    def update_z_mapping(self, z_mapping):
        self.configurations.update_or_create(
            configuration_type='z_mapping',
            defaults={
                'name': '{} Z Mapping'.format(self.uid),
                'json_object': z_mapping
            }
        )
