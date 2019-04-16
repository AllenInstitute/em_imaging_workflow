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
from django.conf import settings
from rendermodules.dataimport.schemas import GenerateMipMapsParameters
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
from django_fsm import can_proceed
import logging


class GenerateMipMapsStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies'
        '.generate_mip_maps_strategy')

    def get_input(self, em_mset, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Generate MIPmaps Input')

        em_mset.mipmap_directory = em_mset.get_storage_directory(
            base_storage_directory=settings.MIPMAP_FILE_PATH)
        em_mset.save()

        inp['render'] = RenderStrategyUtils.render_input_dict(em_mset)

        stack_names = \
            TwoDStackNameManager.generate_mip_maps_stacks(em_mset)

        inp['input_stack'] = stack_names['input_stack']
        inp['output_dir'] = em_mset.mipmap_directory
        inp['zValues'] = [ em_mset.section.z_index ]

        return GenerateMipMapsParameters().dump(inp).data

    def on_running(self, task):
        em_mset = task.enqueued_task_object

        # TODO: make this an FsmMixin
        if can_proceed(em_mset.start_processing):
            em_mset.start_processing()
            em_mset.save()
        else:
            GenerateMipMapsStrategy._log.warn('Bad state transition')

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'output_dir')
        em_mset.mipmap_directory =  results['output_dir']
        em_mset.save()
