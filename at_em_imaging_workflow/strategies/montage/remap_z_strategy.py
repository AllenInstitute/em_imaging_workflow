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
from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
from rendermodules.stack.schemas import RemapZsParameters
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
import logging


class RemapZNotMappedStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.montage'
        '.remap_z_not_mapped_strategy')

    from_mapped = False

    def get_input(self, em_mset, storage_directory, task):
        inp = self.get_workflow_node_input_template(task)

        inp['render'] = RenderStrategyUtils.render_input_dict(em_mset)

        inp['overwrite_zlayer'] = True
        inp['close_stack'] = False
        z_index = em_mset.section.z_index
        z_mapping = em_mset.sample_holder.load.configurations.get(
            configuration_type='z_mapping').json_object

        if self.from_mapped:
            inp['zValues'] = [z_mapping[str(z_index)]]
            inp['new_zValues'] = [z_index]
        else:
            inp['zValues'] = [z_index]
            inp['new_zValues'] = [z_mapping[str(z_index)]]

        stack_names = TwoDStackNameManager.remap_z_stacks(em_mset)
        inp['input_stack'] = stack_names['input_stack']
        inp['output_stack'] = stack_names['output_stack']

        return RemapZsParameters().dump(inp).data


class RemapZMappedStrategy(RemapZNotMappedStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.montage'
        '.remap_z_mapped_strategy')

    from_mapped = True


RemapZStrategy = RemapZNotMappedStrategy
