from workflow_engine.strategies.execution_strategy import \
    ExecutionStrategy
from rendermodules.materialize.schemas import \
    MaterializeSectionsParameters
import jinja2
import os
from development.strategies import RENDER_STACK_ROUGH_ALIGN
from development.models.chunk_assignment import ChunkAssignment
from workflow_engine.models.configuration import Configuration
from django.conf import settings
import logging


class MaterializeSectionsStrategy(ExecutionStrategy):
    _strategies_package = 'development.strategies'
    _package = 'development.strategies.rough.materialize_sections_strategy'
    _templates = 'templates'
    _log_configuration_template = 'spark_log4j_template.properties'
    _log = logging.getLogger(_package)

    def get_input(self, chnk_assign, storage_directory, task):
        inp = Configuration.objects.get(
            name='Materialize Sections Input',
            configuration_type='strategy_config').json_object

        chnk = chnk_assign.chunk
        em_mset = chnk_assign.section.montageset_set.first()

        (z_start, z_end) = chnk.z_range()

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
        inp['stack'] = RENDER_STACK_ROUGH_ALIGN % (
            z_start, z_end)

        inp['rootDirectory'] = chnk.get_storage_directory()

        with open(log4j_properties_path, 'w') as file_handle:
            file_handle.write(
                self.create_log_configuration(log4j_log_path))

        inp['spark_files'] = [ log4j_properties_path ]

        mem = 128
        inp['driverMemory'] = str(int(mem)) +  'g'  # TODO roughly memory * ppn

        inp['height'] = em_mset.camera.height
        inp['width']= em_mset.camera.width
        inp['zValues'] = [ em_mset.section.z_index ]

        return MaterializeSectionsParameters().dump(inp).data

    def on_finishing(self, chnk, results, task):
        self.check_key(results, 'pairCount')
        self.set_well_known_file(
            self.get_output_file(task),
            chnk,
            'point_match_output',
            task)

    def create_log_configuration(self, log_file_path):
        env = jinja2.Environment(
           loader=jinja2.PackageLoader(
               MaterializeSectionsStrategy._strategies_package,
               MaterializeSectionsStrategy._templates))
        log4j_template = env.get_template(
            MaterializeSectionsStrategy._log_configuration_template)

        return log4j_template.render(log_file_path=log_file_path)

    def get_task_objects_for_queue(self, chnk):
        return list(ChunkAssignment.objects.filter(
            chunk=chnk))