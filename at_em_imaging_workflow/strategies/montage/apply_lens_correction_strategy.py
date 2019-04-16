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
from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rendermodules.lens_correction.schemas import ApplyLensCorrectionParameters
from workflow_engine.models.well_known_file import WellKnownFile
from .generate_mesh_lens_correction import GenerateMeshLensCorrection
from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
import simplejson as json
import logging


class ApplyLensCorrectionStrategy(InputConfigMixin, ExecutionStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.'
        'montage.apply_lens_correction_strategy')

    def can_transition(self, em_mset, wn=None):
        em_mset.start_processing()
        em_mset.save()

        return True

    #override if needed
    #set the data for the input file
    def get_input(self, em_mset, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Apply Lens Correction Input'
        )

        stack_names = \
            TwoDStackNameManager.apply_lens_correction_stacks(em_mset)

        inp['render'] = RenderStrategyUtils.render_input_dict(em_mset)

        inp['zValues'] = [ em_mset.section.z_index ]
        inp['input_stack'] = stack_names['input_stack']
        inp['output_stack'] = stack_names['output_stack']
        inp['close_stack'] = False

        try:
            self.read_transform_from_configuration(em_mset, inp)
        except ObjectDoesNotExist:
            inp['transform'] = self.read_transform_from_well_known_file()
        except MultipleObjectsReturned as e:
            ApplyLensCorrectionStrategy._log.error(
                "Too many lens correction transform configurations")
            raise(e)

        return ApplyLensCorrectionParameters().dump(inp).data

    def read_transform_from_configuration(self, em_mset, inp):
        conf = em_mset.reference_set.configurations.get(
            configuration_type=GenerateMeshLensCorrection.CONFIGURATION_TYPE)

        output_json = conf.json_object['output_json']

        try:
            inp['maskUrl'] = conf.json_object['maskUrl']
        except:
            pass

        with open(output_json) as j:
            json_data = json.loads(j.read())
            inp['transform'] = json_data

    def read_transform_from_well_known_file(self, em_mset):
        wkf = WellKnownFile.get(em_mset.reference_set, 'description')
        ApplyLensCorrectionStrategy._log.info('WKF: %s' % (wkf))

        with open(wkf) as j:
            json_data = json.loads(j.read())
            transform = json_data['transform']

        return transform
