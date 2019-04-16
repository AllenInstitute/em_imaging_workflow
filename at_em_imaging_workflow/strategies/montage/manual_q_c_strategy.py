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
from rendermodules.em_montage_qc.schemas import (
    DetectMontageDefectsParameters,
    DetectMontageDefectsParametersOutput
)
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
from django.conf import settings
import logging
import shutil
import os


class ManualQCStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies'
        '.montage.manual_qc_strategy')

    def get_input(self, em_mset, storage_directory, task):
        '''
        Args:
            em_mset : EMMontageSet
        '''
        inp = self.get_workflow_node_input_template(
            task,
            name='Detect Montage Defects Input')

        stack_names = \
            TwoDStackNameManager.detect_defects_stacks(em_mset)

        inp['render'] = RenderStrategyUtils.render_input_dict(em_mset)

        inp['prestitched_stack'] = stack_names['prestitched_stack']
        inp['poststitched_stack'] = stack_names['poststitched_stack']

        inp['minZ'] = em_mset.section.z_index
        inp['maxZ'] = em_mset.section.z_index

        if inp['match_collection'] == '':
            inp['match_collection'] = em_mset.get_point_collection_name()

        inp['out_html_dir'] = storage_directory

        data = DetectMontageDefectsParameters().dump(inp).data

        return data

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'qc_passed_sections')

        z_index = em_mset.section.z_index

        if z_index in results['qc_passed_sections']:
            em_mset.pass_qc()
        elif z_index in results['gap_sections'] or \
           z_index in results['seam_sections'] or \
           z_index in results['hole_sections']:
            if em_mset.object_state == 'REDO_POINT_MATCH':
                em_mset.fail_qc()
            elif em_mset.object_state == 'REDO_SOLVER':
                em_mset.fail_qc()
            elif em_mset.object_state == 'MONTAGE_QC_PASSED':
                pass  # manually passed, don't override
            else:
                em_mset.fail_qc()
        else:
            em_mset.fail_qc()
        em_mset.save()

        try:
            os.makedirs(em_mset.get_storage_directory())
        except:
            pass

        well_known_file_path = \
            os.path.join(
                em_mset.get_storage_directory(),
                'defect_detection_output.json')
        shutil.copy(self.get_output_file(task),
                    well_known_file_path)

        self.set_well_known_file(
            well_known_file_path,
            em_mset,
            'defect_detection',
            task)
