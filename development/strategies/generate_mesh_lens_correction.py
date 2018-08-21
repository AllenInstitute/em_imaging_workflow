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
from workflow_engine.workflow_controller import WorkflowController
from development.strategies import RENDER_STACK_MESH_LENS_RAW,\
    RENDER_STACK_MESH_LENS_CORRECTED, RENDER_LENS_COLLECTION
from rendermodules.mesh_lens_correction.schemas \
    import MeshLensCorrectionSchema
from development.models.reference_set import ReferenceSet
from workflow_engine.models.configuration import Configuration
from django.conf import settings
from development.models import state_machines
import simplejson as json
import logging
import os


class GenerateMeshLensCorrection(ExecutionStrategy):
    CONFIGURATION_TYPE='lens correction transform'
    TRANSFORM='transform'
    _log = logging.getLogger(
        'development.strategies.generate_mesh_correction')

    def get_input(self, ref_set, storage_directory, task):
        '''
        Args:
            ref_set : ReferenceSet
        '''
        project_path = ref_set.storage_directory
        GenerateMeshLensCorrection._log.info(
            'project path: %s' % (project_path))

        inp = Configuration.objects.get(
            name='Generate Mesh Lens Correction Input',
            configuration_type='strategy_config').json_object

        inp['render'] = {}
        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = "em_2d_montage_staging" # ref_set.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['input_stack'] = RENDER_STACK_MESH_LENS_RAW
        inp['output_stack'] = RENDER_STACK_MESH_LENS_CORRECTED
        inp['match_collection'] = RENDER_LENS_COLLECTION

        inp['metafile'] = ref_set.metafile
        inp['z_index'] = ref_set.id
        inp['outfile'] = os.path.join(storage_directory,
                                      'lens_correction_out.json')
        inp['output_dir'] = storage_directory
        inp['out_html_dir'] = storage_directory

        if ref_set.workflow_state == 'REDO_LENS_CORRECTION':
            additional_config = self.get_good_solve_from_configuration(ref_set)
            inp.update(additional_config)

        return MeshLensCorrectionSchema().dump(inp).data

    def get_good_solve_from_configuration(
        self, ref_set):
        default_json_obj = {
            'good_solve': {
                'error_mean': 0.2,
                'error_std': 3.0,
                'scale_dev': 0.1 }}
        config, _ = ref_set.configurations.get_or_create(
            configuration_type='ref_set_alternate_parameters',
            defaults={
                'name': 'ref set params for {}'.format(str(ref_set)),
                'json_object': default_json_obj })
        return config.json_object 

    def on_running(self, task):
        ref_set = WorkflowController.get_enqueued_object(task)
        #try:
        #    state_machines.transition(
        #        ref_set,
        #        'workflow_state',
        #        state_machines.states(ref_set).PROCESSING)
        #except Exception as e:
        #    GenerateMeshLensCorrection._log.warn(
        #        'Cannot transfer to processing state')
        ref_set.workflow_state = 'PROCESSING'
        ref_set.save()

    def on_failure(self, task):
        ref_set = WorkflowController.get_enqueued_object(task)

        #state_machines.transition(
        #    ref_set,
        #    'workflow_state',
        #    state_machines.states(ref_set).FAILED)
        ref_set.workflow_state = 'FAILED'
        ref_set.save()

    def on_finishing(self, ref_set, results, task):
        ''' called after the execution finishes
            process and save results to the database
        '''
        self.check_key(results, 'output_json')

        GenerateMeshLensCorrection._log.info(
            'lens_correction_transform output %s' % (str(results)))

        transform_configuration_data = {
            'output_json': results['output_json']
        }

        lens_correction_configuration_name = \
            "lens correction for {}".format(str(ref_set))

        ref_set.configurations.update_or_create(
            configuration_type=GenerateMeshLensCorrection.CONFIGURATION_TYPE,
            defaults={
                'name': lens_correction_configuration_name,
                'json_object': transform_configuration_data })

        #state_machines.transition(
        #    ref_set,
        #    'workflow_state',
        #    state_machines.states(ref_set).DONE)
        ref_set.workflow_state = 'DONE'
        ref_set.save()

        # trigger waiting jobs
        WorkflowController.set_jobs_for_run(
            'Wait for Lens Correction')

    # TODO: this isn't used.  Ingest picks it directly
    def can_transition(self, ref_set):
        is_reference_set = isinstance(ref_set, ReferenceSet)

        return is_reference_set

    #override if needed
    #set the storage directory for an enqueued object
    def get_storage_directory(self, base_storage_directory, job):
        ref_set = job.get_enqueued_object()
        return ref_set.get_storage_directory(base_storage_directory)
