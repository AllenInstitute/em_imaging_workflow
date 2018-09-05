from workflow_engine.strategies.execution_strategy import \
    ExecutionStrategy
from rendermodules.pointmatch.schemas import \
    PointMatchClientParametersSpark
from workflow_engine.models.configuration import Configuration
from workflow_engine.models.well_known_file import WellKnownFile
from django.core.exceptions import ObjectDoesNotExist
import jinja2
import os
from django.conf import settings
import logging

class TwoDMontagePointMatchStrategy(ExecutionStrategy):
    _package = 'development.strategies.two_d_montage_point_match_strategy'
    _templates = 'templates'
    _log_configuration_template = 'spark_log4j_template.properties'
    _log = logging.getLogger(_package)

    def get_input(self, em_mset, storage_directory, task):
        inp = Configuration.objects.get(
            name='2D Montage Point Match Input',
            configuration_type='strategy_config').json_object

        inp['sparkhome'] = settings.SPARK_HOME
        log_dir = self.get_or_create_task_storage_directory(task)
        inp['logdir'] = log_dir

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = em_mset.get_render_project_name()
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

        inp['collection'] = em_mset.get_point_collection_name()
        inp['pairJson'] = self.get_tile_pairs_file_name(em_mset)

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

        if em_mset.object_state == 'REDO_POINT_MATCH':
            inp['renderScale'] = self.get_render_scale_from_configuration(
                em_mset,
                inp['renderScale'])

        return PointMatchClientParametersSpark().dump(inp).data

    def get_tile_pairs_file_name(self, em_mset):
        return WellKnownFile.get(
            em_mset,
            em_mset.tile_pairs_file_description())

    def get_render_scale_from_configuration(self, em_mset, initial_render_scale):
        try:
            config = em_mset.configurations.get(
                configuration_type='point_match_parameters')
        except ObjectDoesNotExist:
            point_match_state = {
                'render_scale': initial_render_scale
            }
            config = Configuration(
                content_object=em_mset,
                name='point match params for {}'.format(str(em_mset)),
                configuration_type='point_match_parameters',
                json_object=point_match_state)

        render_scale = 0.5
        config.json_object['render_scale'] = 0.5
        config.save()

        return render_scale

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'pairCount')
        self.set_well_known_file(
            self.get_output_file(task),
            em_mset,
            'point_match_output',
            task)

    def create_log_configuration(self, log_file_path):
        env = jinja2.Environment(
           loader=jinja2.PackageLoader(
               TwoDMontagePointMatchStrategy._package,
               TwoDMontagePointMatchStrategy._templates))
        log4j_template = env.get_template(
            TwoDMontagePointMatchStrategy._log_configuration_template)

        return log4j_template.render(log_file_path=log_file_path)

