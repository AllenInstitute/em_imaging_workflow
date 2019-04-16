from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from rendermodules.pointmatch.schemas import PointMatchClientParametersSpark
from at_em_imaging_workflow.models import ChunkAssignment
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
import jinja2
import os
from django.conf import settings
import logging

def add_arg(l,argname,args):
    value = args.get(argname,None)
    if value is not None:
        l+=["--{}".format(argname),"{}".format(args[argname])]


def form_sift_params_list(args):
    sift_params = []

    for arg in (
        'baseDataUrl',
        'collection',
        'owner',
        'SIFTfdSize',
        'SIFTsteps',
        'matchMaxEpsilon',
        'maxFeatureCacheGb',
        'SIFTminScale',
        'SIFTmaxScale',
        'renderScale',
        'matchRod',
        'matchMinInlierRatio',
        'matchMinNumInliers',
        'matchMaxNumInliers',
        'clipWidth',
        'clipHeight',
        'pairJson'
    ):
        add_arg(sift_params, arg, args)

    return sift_params


class RoughPointMatchStrategy(InputConfigMixin, ExecutionStrategy):
    _package = ('at_em_imaging_workflow.strategies.montage.'
                'two_d_montage_point_match_strategy')
    _templates = 'templates'
    _log_configuration_template = 'spark_log4j_template.properties'
    _log = logging.getLogger(_package)

    def get_input_dict(self, chnk_assn, task):
        inp = self.get_workflow_node_input_template(
            task,
            name="EM Rough Point Match Input"
        )
        chnk = chnk_assn.chunk
 
        inp['owner'] = settings.RENDER_SERVICE_USER
        inp['jarfile'] = settings.RENDER_SPARK_JARFILE
        inp['collection'] = TwoDStackNameManager.rough_point_match_collection(
            chnk
        )
        inp['pairJson'] = chnk_assn.get_rough_tile_pair_file_name()
 
        inp['sparkhome'] = settings.SPARK_HOME
 
        mem = 128
        ppn = 24
        # inp['memory'] = str(int((mem - ppn) / ppn)) + 'g'
        inp['driverMemory'] = str(int(mem)) +  'g'  # TODO roughly memory * ppn
        inp['maxFeatureCacheGb'] = 3
 
        #retries = 20
        # inp['masterUrl'] = 'local[*,%d]' % (retries)
        inp['baseDataUrl'] = "{}:{}/render-ws/v1".format(
            settings.RENDER_SERVICE_URL,
            settings.RENDER_SERVICE_PORT
        )

        return inp

    def get_render_dict(self, chnk):
        return {
            'host': settings.RENDER_SERVICE_URL,
            'port': settings.RENDER_SERVICE_PORT,
            'owner': settings.RENDER_SERVICE_USER,
            'project': chnk.get_render_project_name(),
            'client_scripts': settings.RENDER_CLIENT_SCRIPTS
        }

    def get_logging_dict(self, task, write_files=True):
        log_dir = self.get_or_create_task_storage_directory(task)

        log4j_properties_path = os.path.join(log_dir, 'log4j.properties')
        log4j_log_path = os.path.join(log_dir, 'spark.log')

        if write_files:
            self.write_spark_log_files(
                log4j_properties_path,
                log4j_log_path
            )

        return {
            'logdir': log_dir,
            'spark_files': [ log4j_properties_path ],
            'spark_conf': {
            'spark.driver.extraJavaOptions':
                '-Dlog4j.configuration=file:%s' % (log4j_properties_path) }
        }

    def write_spark_log_files(self, log4j_properties_path, log4j_log_path):
        with open(log4j_properties_path, 'w') as file_handle:
            file_handle.write(
                self.create_log_configuration(log4j_log_path))

    def get_input_file(self, task):
        return None

    def get_output_file(self, task):
        return None

    def get_input(self, chnk_assn, storage_directory, task):
        chnk = chnk_assn.chunk
 
        inp = self.get_input_dict(chnk_assn, task)
        inp['render'] = self.get_render_dict(chnk)
        inp.update(self.get_logging_dict(task, write_files=False))
 
        return PointMatchClientParametersSpark().dump(inp).data

    def get_task_arguments(self, task, write_files=False):
        chnk_assn = task.enqueued_task_object
        chnk = chnk_assn.chunk

        inp = self.get_input_dict(chnk_assn, task)
        inp['render'] = self.get_render_dict(chnk)
        inp.update(self.get_logging_dict(task, write_files))

        return form_sift_params_list(inp)

    def on_finishing(self, chnk_assn, results, task):
        if 'pairCount' in results:
            chnk_assn.update_tile_pair_file(
                pair_count=results['pairCount'],
                # point_match_output=self.get_output_file(task)
            )
        else:
            # TODO: check if this is still needed
            RoughPointMatchStrategy._log.warn(
                'Pair count not found')

    def create_log_configuration(self, log_file_path):
        env = jinja2.Environment(
           loader=jinja2.PackageLoader(
               RoughPointMatchStrategy._package,
               RoughPointMatchStrategy._templates))
        log4j_template = env.get_template(
            RoughPointMatchStrategy._log_configuration_template)

        return log4j_template.render(log_file_path=log_file_path)

    def get_task_objects_for_queue(self, chnk):
        tile_pair_ranges = chnk.get_tile_pair_ranges()

        chunk_assignments = [
            ChunkAssignment.objects.get(
                chunk=chnk,
                section=chnk.sections.get(
                    z_index=tile_pair_ranges[x]['tempz'])
            ) for x in tile_pair_ranges.keys()]

        return chunk_assignments

    def get_storage_directory(self, base_storage_directory, job):
        chnk = job.enqueued_object

        return chnk.get_storage_directory(base_storage_directory)
