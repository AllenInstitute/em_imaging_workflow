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
from workflow_engine.strategies.execution_strategy import ExecutionStrategy
from rendermodules.lens_correction.schemas \
    import LensCorrectionParameters
from development.strategies.schemas.generate_lens_correction_transform import input_dict
from django.conf import settings
import logging
import os


class GenerateLensCorrectionTransformStrategy(ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.generate_lens_correction_transform_strategy')

    # def skip_execution(self, enqueued_object):
    #    return True

    #override if needed
    #set the data for the input file
    def get_input(self, enqueued_object, storage_directory, task):
        '''
        Args:
            enqueued_object (ReferenceSet)
        '''
        project_path = enqueued_object.storage_directory
        GenerateLensCorrectionTransformStrategy._log.info(
            'project path: %s' % (project_path))
        
        inp = input_dict 

        inp['manifest_path'] = enqueued_object.manifest_path
        inp['project_path'] = project_path
        inp['fiji_path'] = settings.FIJI_PATH
        inp['outfile'] = os.path.join(storage_directory,
                                        'lens_correction_out.json')
        inp['processing_directory'] = storage_directory

        return LensCorrectionParameters().dump(inp).data

    def on_finishing(self, enqueued_object, results, task):
        ''' called after the execution finishes
            process and save results to the database
        '''
        self.check_key(results, 'output_json')

        GenerateLensCorrectionTransformStrategy._log.info(
            'lens_correction_transform output %s' % (str(results)))
        self.set_well_known_file(
            results['output_json'],
            enqueued_object,
            'description',
            task)

    #override if needed
    #set the storage directory for an enqueued object
    def get_storage_directory(self, base_storage_directory, job):
        enqueued_object = job.get_enqueued_object()
        return os.path.join(base_storage_directory,
                            'reference_set_' + str(enqueued_object.id))
