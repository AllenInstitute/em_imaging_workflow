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
from workflow_engine.workflow_controller import WorkflowController
from at_em_imaging_workflow.strategies import (
    RENDER_STACK_MESH_LENS_RAW,
    RENDER_STACK_MESH_LENS_CORRECTED,
    RENDER_LENS_COLLECTION
)
from rendermodules.mesh_lens_correction.schemas import (
    MeshLensCorrectionSchema
)
from at_em_imaging_workflow.models.reference_set import ReferenceSet
from django_fsm import can_proceed
import logging
import os


class GenerateMeshLensCorrection(InputConfigMixin, ExecutionStrategy):
    CONFIGURATION_TYPE='lens correction transform'
    CONFIGURATION_NAME='Generate Mesh Lens Correction Input'
    TEMCA3_CONFIGURATION='Generate Mesh Lens Correction TEMCA3 Input'
    BAD_CORNER_50MP_CONFIGURATION=TEMCA3_CONFIGURATION
    TEMCA2_50MP_CAMERA_ID='BJMAB1820029'
    TRANSFORM='transform'
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.montage.'
        'generate_mesh_correction')

    def get_input(self, ref_set, task_storage_directory, task):
        '''
        Args:
            ref_set : ReferenceSet
        '''
        project_path = ref_set.storage_directory
        GenerateMeshLensCorrection._log.info(
            'project path: %s' % (project_path))

        inp = self.get_workflow_node_input_template(task)

        inp['render'] = RenderStrategyUtils.render_input_dict(ref_set)

        inp['input_stack'] = RENDER_STACK_MESH_LENS_RAW
        inp['output_stack'] = RENDER_STACK_MESH_LENS_CORRECTED
        inp['match_collection'] = RENDER_LENS_COLLECTION

        inp['metafile'] = ref_set.metafile
        inp['z_index'] = ref_set.id
        inp['outfile'] = os.path.join(task_storage_directory,
                                      'lens_correction_out.json')
        inp['output_dir'] = task_storage_directory
        inp['out_html_dir'] = task_storage_directory
        inp['mask_dir'] = ref_set.get_storage_directory()

        if ref_set.object_state == ReferenceSet.STATE.LENS_CORRECTION_REDO:
            additional_config = self.get_good_solve_from_configuration(ref_set)
            inp.update(additional_config)

        # input_data_json = MeshLensCorrectionSchema().dump(inp).data
        input_data_json = inp

        do_montage_qc = self.get_do_montage_qc(ref_set)

        if do_montage_qc is not None:
            input_data_json['do_montage_QC'] = do_montage_qc

        return input_data_json

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

    def get_do_montage_qc(self, ref_set):
        try:
            config = ref_set.configurations.get(
                configuration_type='ref_set_alternate_parameters').json_object
            if 'do_montage_QC' in config:
                return config['do_montage_QC']
            else:
                return None
        except:
            return None


    def on_running(self, task):
        ref_set = task.enqueued_task_object
        ref_set.start_processing()
        ref_set.save()

    def on_failure(self, task):
        ref_set = task.enqueued_task_object
        if can_proceed(ref_set.reset_pending):
            ref_set.reset_pending()
            ref_set.save()

    def on_finishing(self, ref_set, results, task):
        ''' called after the execution finishes
            process and save results to the database
        '''
        if can_proceed(ref_set.finish_processing):
            self.check_key(results, 'output_json')
            self.check_key(results, 'maskUrl')

            GenerateMeshLensCorrection._log.info(
                'lens_correction_transform output %s' % (str(results)))

            transform_configuration_data = {
                'output_json': results['output_json'],
                'maskUrl': results['maskUrl']
            }

            lens_correction_configuration_name = \
                "lens correction for {}".format(str(ref_set))

            ref_set.configurations.update_or_create(
                configuration_type=GenerateMeshLensCorrection.CONFIGURATION_TYPE,
                defaults={
                    'name': lens_correction_configuration_name,
                    'json_object': transform_configuration_data 
                }
            )

            ref_set.finish_processing()
            ref_set.save()

            # trigger waiting jobs
            WorkflowController.set_jobs_for_run(
                'Wait for Lens Correction'
            )

    # TODO: this isn't used.  Ingest picks it directly
    def can_transition(self, ref_set):
        is_reference_set = isinstance(ref_set, ReferenceSet)

        return is_reference_set

    #override if needed
    #set the storage directory for an enqueued object
    def get_storage_directory(self, base_storage_directory, job):
        ref_set = job.enqueued_object

        return ref_set.get_storage_directory(base_storage_directory)
