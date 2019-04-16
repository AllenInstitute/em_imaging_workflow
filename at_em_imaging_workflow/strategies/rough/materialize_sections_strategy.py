from django.conf import settings
from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from rendermodules.materialize.schemas import (
    MaterializeSectionsParameters
)
from at_em_imaging_workflow.two_d_stack_name_manager import (
    TwoDStackNameManager
)
import jinja2
import os
import logging


class MaterializeSectionsStrategy(InputConfigMixin, ExecutionStrategy):
    _strategies_package = 'at_em_imaging_workflow.strategies'
    _package = 'at_em_imaging_workflow.strategies.rough.materialize_sections_strategy'
    _templates = 'templates'
    _log_configuration_template = 'spark_log4j_template.properties'
    _log = logging.getLogger(_package)

    def get_objects_for_queue(self, prev_queue_job):
        chnk = prev_queue_job.enqueued_object

        return list(chnk.chunkassignment_set.all())

    def get_input(self, chnk_assign, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='Materialize Sections Input')

        chnk = chnk_assign.chunk
        em_mset = chnk_assign.section.montageset_set.first()

        # TODO: test and consolidate
        chunk_load = chnk.get_load()
        z_mapping = chnk.get_z_mapping(chunk_load)
        tile_pair_ranges = chnk.get_tile_pair_ranges()
        min_z, max_z = chnk.calculate_z_min_max(tile_pair_ranges)
        clipped_z_mapping = chnk.clip_z_mapping_to_min_max(
                z_mapping, min_z, max_z)

        #mapped_from = clipped_z_mapping.keys()

        #old_zs = [int(z) for z in mapped_from]
        #new_zs = [clipped_z_mapping[z] for z in mapped_from]

        inp['sparkhome'] = settings.SPARK_HOME
        log_dir = self.get_or_create_task_storage_directory(task)
        log4j_properties_path = os.path.join(log_dir, 'log4j.properties')
        log4j_log_path = os.path.join(log_dir, 'spark.log')
        inp['spark_conf'] = {
            'spark.driver.extraJavaOptions':
                '-Dlog4j.configuration=file:%s' % (log4j_properties_path) }

        retries = 20
        inp['masterUrl'] = 'local[*,%d]' % (retries)
        inp['jarfile'] = settings.RENDER_SPARK_JARFILE
        inp['baseDataUrl'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ':' + settings.RENDER_SERVICE_PORT + '/render-ws/v1'
        inp['owner'] = settings.RENDER_SERVICE_USER
        inp['project'] = chnk.get_render_project_name()
        inp['stack'] = TwoDStackNameManager.RENDER_STACK_FUSION

        # TODO: Generalize
        if (chnk.computed_index == 35):
            inp['stack'] = 'FUSEDOUTPUTSTACK_Chunk_30_31_33'

        inp['rootDirectory'] = chnk.get_storage_directory()

        with open(log4j_properties_path, 'w') as file_handle:
            file_handle.write(
                self.create_log_configuration(log4j_log_path))

        inp['spark_files'] = [ log4j_properties_path ]

        mem = 128
        # inp['driverMemory'] = str(int(mem)) +  'g'  # TODO roughly memory * ppn

        mapped_z = clipped_z_mapping[str(em_mset.section.z_index)]
        inp['zValues'] = [ mapped_z ]

        return MaterializeSectionsParameters().dump(inp).data

#     def on_finishing(self, chnk, results, task):
#         self.check_key(results, 'pairCount')
#         self.set_well_known_file(
#             self.get_output_file(task),
#             chnk,
#             'point_match_output',
#             task)

    def create_log_configuration(self, log_file_path):
        env = jinja2.Environment(
           loader=jinja2.PackageLoader(
               MaterializeSectionsStrategy._strategies_package,
               MaterializeSectionsStrategy._templates))
        log4j_template = env.get_template(
            MaterializeSectionsStrategy._log_configuration_template)

        return log4j_template.render(log_file_path=log_file_path)
