from workflow_engine.strategies.execution_strategy import \
    ExecutionStrategy
from rendermodules.pointmatch.schemas import \
    PointMatchClientParametersSpark
import copy
from workflow_engine.models.well_known_file import WellKnownFile
import jinja2
import os
from development.strategies.chmod_strategy import ChmodStrategy
from development.strategies.schemas.rough.rough_point_match \
    import input_dict
from django.conf import settings
import logging

class RoughPointMatchStrategy(ExecutionStrategy):
    _package = 'development.strategies.two_d_montage_point_match_strategy'
    _templates = 'templates'
    _log_configuration_template = 'spark_log4j_template.properties'
    _log = logging.getLogger(_package)

    def get_input(self, chnk, storage_directory, task):
        RoughPointMatchStrategy._log.info("get input")

        inp = copy.deepcopy(input_dict)

        inp['sparkhome'] = settings.SPARK_HOME
        log_dir = self.get_or_create_task_storage_directory(task)
        inp['logdir'] = log_dir

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = 'FIXME' # chnk.get_render_project_name()
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
        inp['pairJson'] = self.get_tile_pairs_file_name(chnk)

        mem = 128
        ppn = 24
        inp['memory'] = str(int((mem - ppn) / ppn)) + 'g'
        inp['driverMemory'] = str(int(mem)) +  'g'  # TODO roughly memory * ppn

        clipWidth = 800
        clipHeight = 800
        inp['clipWidth'] = clipWidth
        inp['clipHeight'] = clipHeight
        inp['maxFeatureCacheGb'] = 3

        retries = 20
        inp['masterUrl'] = 'local[*,%d]' % (retries)
        inp['baseDataUrl'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ':' + settings.RENDER_SERVICE_PORT + '/render-ws/v1'

        return PointMatchClientParametersSpark().dump(inp).data

    def get_tile_pairs_file_name(self, chnk):
        return WellKnownFile.get(
            chnk,
            chnk.tile_pairs_file_description())

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'pairCount')
        self.set_well_known_file(
            self.get_output_file(task),
            em_mset,
            'point_match_output',
            task)
        d = self.get_or_create_task_storage_directory(task)
        ChmodStrategy.add_chmod_file(em_mset, d)
        ChmodStrategy.add_chmod_dir(em_mset, d)
        ChmodStrategy.enqueue_montage(em_mset)

    def create_log_configuration(self, log_file_path):
        env = jinja2.Environment(
           loader=jinja2.PackageLoader(
               RoughPointMatchStrategy._package,
               RoughPointMatchStrategy._templates))
        log4j_template = env.get_template(
            RoughPointMatchStrategy._log_configuration_template)

        return log4j_template.render(log_file_path=log_file_path)

