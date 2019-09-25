# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2018-2019. Allen Institute. All rights reserved.
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
from workflow_engine.strategies import (
    InputConfigMixin,
    ExecutionStrategy
)
from at_em_imaging_workflow.render_strategy_utils import (
    RenderStrategyUtils
)
from rendermodules.dataimport.schemas import (
    MakeMontageScapeSectionStackParameters
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
from django.conf import settings
import logging


class MakeMontageScapesStackStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.montage'
        '.make_montage_scapes_stack_strategy')

    def get_input(self, em_mset, storage_directory, task):
        inp = self.get_workflow_node_input_template(task)

        inp['render'] = RenderStrategyUtils.render_input_dict(em_mset)

        inp['set_new_z'] = True
        z_index = em_mset.section.z_index
        inp['minZ'] = z_index
        inp['maxZ'] = z_index

        z_mapping = em_mset.sample_holder.load.configurations.get(
            configuration_type='z_mapping').json_object
        inp['new_z_start'] = z_mapping[str(z_index)]

        inp['image_directory'] = em_mset.get_storage_directory(
            settings.LONG_TERM_BASE_FILE_PATH
        )

        stack_names = TwoDStackNameManager.make_montage_scapes_stacks(em_mset)
        inp['montage_stack'] = stack_names['montage_stack']
        inp['output_stack'] = stack_names['output_stack']

        return MakeMontageScapeSectionStackParameters().dump(inp)
