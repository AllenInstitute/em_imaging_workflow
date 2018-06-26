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
from workflow_engine.strategies import execution_strategy
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rendermodules.lens_correction.schemas import \
  ApplyLensCorrectionParameters
from workflow_engine.models.configuration import Configuration
from workflow_engine.models.well_known_file import WellKnownFile
from django.conf import settings
import simplejson as json
import logging
from development.strategies.generate_mesh_lens_correction \
    import GenerateMeshLensCorrection
from development.strategies \
    import RENDER_STACK_APPLY_MIPMAPS, RENDER_STACK_LENS_CORRECTED


class ApplyLensCorrectionStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.apply_lens_correction_strategy')
    
    #override if needed
    #set the data for the input file
    def get_input(self, em_mset, storage_directory, task):
        inp = Configuration.objects.get(
            name='Apply Lens Correction Input',
            configuration_type='strategy_config').json_object

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS
        inp['zValues'] = [ em_mset.section.z_index ]
        inp['input_stack'] = RENDER_STACK_APPLY_MIPMAPS
        inp['output_stack'] = RENDER_STACK_LENS_CORRECTED
        inp['close_stack'] = False

        try:
            inp['transform'] = self.read_transform_from_configuration(em_mset)
        except ObjectDoesNotExist:
            inp['transform'] = self.read_transform_from_well_known_file()
        except MultipleObjectsReturned as e:
            ApplyLensCorrectionStrategy._log.error(
                "Too many lens correction transform configurations")
            raise(e)

        return ApplyLensCorrectionParameters().dump(inp).data

    def read_transform_from_configuration(self, em_mset):
        conf = em_mset.reference_set.configurations.get(
            configuration_type=GenerateMeshLensCorrection.CONFIGURATION_TYPE)

        return conf.json_object[GenerateMeshLensCorrection.TRANSFORM]

    def read_transform_from_well_known_file(self, em_mset):
        wkf = WellKnownFile.get(em_mset.reference_set, 'description')
        ApplyLensCorrectionStrategy._log.info('WKF: %s' % (wkf))

        with open(wkf) as j:
            json_data = json.loads(j.read())
            transform = json_data['transform']
        
        return transform
