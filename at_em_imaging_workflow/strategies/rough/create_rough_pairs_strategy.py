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
from at_em_imaging_workflow.models import ChunkAssignment
from rendermodules.pointmatch.schemas import TilePairClientParameters
from django.conf import settings
import logging
from at_em_imaging_workflow.models import Chunk
from workflow_engine.strategies import (
    ExecutionStrategy,
    InputConfigMixin
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)


class CreateRoughPairsStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.rough.'
        'create_rough_pairs_strategy')

    def can_transition(self, enqueued_object, source_node=None):
        if type(enqueued_object) is Chunk:
            return True

        return False

    def get_objects_for_queue(self, prev_queue_job):
        objects = []
        objects.append(prev_queue_job.enqueued_object)

        return objects

    def get_input(self, chk_assgn, storage_directory, task):
        inp = self.get_workflow_node_input_template(task)

        chnk = chk_assgn.chunk

        stack_names = \
            TwoDStackNameManager.create_rough_pair_stacks(
                chk_assgn)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['output_dir'] = chnk.get_storage_directory()

        tile_pair_ranges = chnk.get_tile_pair_ranges()

        section_z_index = chk_assgn.section.z_index

        for k in tile_pair_ranges.keys():
            tile_pair_range = tile_pair_ranges[k]
            if tile_pair_range['tempz'] == section_z_index:
                min_z = tile_pair_range['minz']
                max_z = tile_pair_range['maxz']

                inp["minZ"] = min_z
                inp["maxZ"] = max_z
                inp["zNeighborDistance"] = tile_pair_range["zNeighborDistance"]

        inp['baseStack'] = stack_names['baseStack']
        inp['stack'] = stack_names['stack']

        return TilePairClientParameters().dump(inp).data

    def on_finishing(self, chk_assgn, results, task):
        self.check_key(results, ChunkAssignment.TILE_PAIR_FILE_KEY)
        chk_assgn.create_rough_tile_pair_file(
            results[ChunkAssignment.TILE_PAIR_FILE_KEY]
        )

    def get_task_objects_for_queue(self, chnk):
        tile_pair_ranges = chnk.get_tile_pair_ranges()

        chunk_assignments = [
            ChunkAssignment.objects.get(
                chunk=chnk,
                section__z_index=tile_pair_ranges[x]['tempz']
            ) for x in tile_pair_ranges.keys()]

        return chunk_assignments

    def get_storage_directory(self, base_storage_directory, job):
        chnk = job.enqueued_object

        return chnk.get_storage_directory(base_storage_directory)

