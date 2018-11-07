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
from workflow_engine.strategies import execution_strategy
from rendermodules.pointmatch_filter.schemas import (
    FilterSchema
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
from workflow_engine.workflow_controller import (
    WorkflowController
)
from development.strategies import (
    get_workflow_node_input_template
)
import logging


class FilterPointMatchStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'montage.filter_point_match_strategy')

    def can_transition(self, em_mset):
        return em_mset.microscope.uid == 'temca4'

    def get_input(self, em_mset, storage_directory, task):
        inp = get_workflow_node_input_template(task)

        inp['render'].update(
            TwoDStackNameManager.em_montage_set_render_settings(
                em_mset
            )
        )

        inp.update(
            TwoDStackNameManager.filter_point_match_stacks(em_mset)
        )

        inp['minZ'] = em_mset.section.z_index
        inp['maxZ'] = em_mset.section.z_index

        return FilterSchema().dump(inp).data

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'filter_output_file')

        filter_output = {
            'filter_output_file': results['filter_output_file']
        }

        config,_ = em_mset.configurations.get_or_create(
            configuration_type='em_montage_set_info',
            name='info for {}'.format(str(em_mset)),
            defaults={
                'json_object': {}
            }
        )
        config.json_object.update(filter_output)
        config.save()

        WorkflowController.start_workflow_2(
            'em_2d_montage',
            em_mset,
            start_node_name='2D Montage Python Solver',
            reuse_job=True,
            raise_priority=True)


