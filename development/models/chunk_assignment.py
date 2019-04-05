# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2018. Allen Institute. All rights reserved.
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
from workflow_engine.mixins import Enqueueable


class ChunkAssignment(Enqueueable, models.Model):
    section = models.ForeignKey('Section')
    chunk = models.ForeignKey('Chunk')

    ROUGH_TILE_PAIR_FILE = 'rough_tile_pair_file'
    TILE_PAIR_FILE_KEY = 'tile_pair_file'
    PAIR_COUNT_KEY = 'pairCount'
    POINT_MATCH_OUTPUT = 'point_match_output'

    def __str__(self):
        return "%s in %s" % (str(self.section), str(self.chunk))

    def storage_basename(self):
        return '{}_z{}_{}'.format(
            self.chunk.computed_index,
            self.section.z_index
        )

    def create_rough_tile_pair_file(self, tile_pair_file):
        z_index = str(self.section.z_index)

        cfg, created = self.chunk.configurations.get_or_create(
            configuration_type=ChunkAssignment.ROUGH_TILE_PAIR_FILE
        )

        if created:
            cfg.json_object = {
                z_index: {
                    ChunkAssignment.TILE_PAIR_FILE_KEY: tile_pair_file
                }
            }
        else:
            cfg.json_object[z_index] = {
                ChunkAssignment.TILE_PAIR_FILE_KEY: tile_pair_file
            }

        cfg.name='Rough Tile Pair File for Chunk {}'.format(
            self.chunk.computed_index
        )

        cfg.save()

    def update_tile_pair_file(self,
                              pair_count=None,
                              point_match_output=None):
        chnk = self.chunk
        z_index = str(self.section.z_index)

        tile_pair_cfg = chnk.configurations.get(
            configuration_type=ChunkAssignment.ROUGH_TILE_PAIR_FILE)
        tile_pair_json = tile_pair_cfg.json_object

        if pair_count:
            tile_pair_json[z_index][
                ChunkAssignment.PAIR_COUNT_KEY
            ] = pair_count
        if point_match_output:
            tile_pair_json[z_index][
                ChunkAssignment.POINT_MATCH_OUTPUT
            ] = point_match_output
        #tile_pair_cfg.json_object = tile_pair_json
        tile_pair_cfg.save()

    def get_rough_tile_pair_file_name(self):
        tile_pair_cfg = self.chunk.configurations.get(
            configuration_type=ChunkAssignment.ROUGH_TILE_PAIR_FILE
        ).json_object
        tile_pair_file_name = tile_pair_cfg[
            str(self.section.z_index)
        ][ChunkAssignment.TILE_PAIR_FILE_KEY]

        return tile_pair_file_name
