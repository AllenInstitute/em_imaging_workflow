from workflow_engine.strategies.execution_strategy import \
    ExecutionStrategy
from development.strategies \
    import get_workflow_node_input_template
from rendermodules.pointmatch.schemas import \
    PointMatchClientParametersSpark
from development.models.chunk_assignment import ChunkAssignment
from development.strategies.rough.solve_rough_alignment_strategy \
    import SolveRoughAlignmentStrategy
from workflow_engine.models.well_known_file import WellKnownFile
import jinja2
import os
from django.conf import settings
import logging

class RoughPointMatchStrategy(ExecutionStrategy):
    _package = 'development.strategies.two_d_montage_point_match_strategy'
    _templates = 'templates'
    _log_configuration_template = 'spark_log4j_template.properties'
    _log = logging.getLogger(_package)

    def get_input(self, chnk_assgn, storage_directory, task):
        inp = get_workflow_node_input_template(task)

        chnk = chnk_assgn.chunk
        z_index = chnk_assgn.section.z_index

        inp['sparkhome'] = settings.SPARK_HOME
        log_dir = self.get_or_create_task_storage_directory(task)
        inp['logdir'] = log_dir

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['owner'] = settings.RENDER_SERVICE_USER

        inp['jarfile'] = settings.RENDER_SPARK_JARFILE

        log4j_properties_path = os.path.join(log_dir, 'log4j.properties')
        log4j_log_path = os.path.join(log_dir, 'spark.log')

        with open(log4j_properties_path, 'w') as file_handle:
            file_handle.write(
                self.create_log_configuration(log4j_log_path))

        inp['spark_files'] = [ log4j_properties_path ]
        inp['spark_conf'] = {
            'spark.driver.extraJavaOptions':
                '-Dlog4j.configuration=file:%s' % (log4j_properties_path) }

        inp['collection'] = chnk.get_point_collection_name()

        tile_pair_cfg = chnk.configurations.get(
            configuration_type='rough_tile_pair_file').json_object
        tile_pair_file_name = tile_pair_cfg[str(z_index)]['tile_pair_file']
        inp['pairJson'] = tile_pair_file_name # self.get_tile_pairs_file_name(chnk)

        mem = 128
        ppn = 24
        # inp['memory'] = str(int((mem - ppn) / ppn)) + 'g'
        inp['driverMemory'] = str(int(mem)) +  'g'  # TODO roughly memory * ppn

        inp['maxFeatureCacheGb'] = 3

        retries = 20
        inp['masterUrl'] = 'local[*,%d]' % (retries)
        inp['baseDataUrl'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ':' + settings.RENDER_SERVICE_PORT + '/render-ws/v1'

        return PointMatchClientParametersSpark().dump(inp).data

    # TODO: deprecated
    def get_tile_pairs_file_name(self, chnk):
        return WellKnownFile.get(
            chnk,
            chnk.tile_pairs_file_description())

    def on_finishing(self, chnk_assgn, results, task):
        self.check_key(results, 'pairCount')

        chnk = chnk_assgn.chunk
        z_index = chnk_assgn.section.z_index

        tile_pair_cfg = chnk.configurations.get(
            configuration_type='rough_tile_pair_file')
        tile_pair_json = tile_pair_cfg.json_object
        
        tile_pair_json[str(z_index)]['pairCount'] = \
            results['pairCount']
        tile_pair_json[str(z_index)]['point_match_output'] = \
            self.get_output_file(task)
        #tile_pair_cfg.json_object = tile_pair_json
        tile_pair_cfg.save()


    def create_log_configuration(self, log_file_path):
        env = jinja2.Environment(
           loader=jinja2.PackageLoader(
               RoughPointMatchStrategy._package,
               RoughPointMatchStrategy._templates))
        log4j_template = env.get_template(
            RoughPointMatchStrategy._log_configuration_template)

        return log4j_template.render(log_file_path=log_file_path)

    def get_task_objects_for_queue(self, chnk):
        tile_pair_ranges = \
            SolveRoughAlignmentStrategy.get_tile_pair_ranges(chnk)

        chunk_assignments = [
            ChunkAssignment.objects.get(
                chunk=chnk,
                section=chnk.sections.get(
                    z_index=tile_pair_ranges[x]['tempz'])
            ) for x in tile_pair_ranges.keys()]

        return chunk_assignments

