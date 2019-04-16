from workflow_engine.strategies import InputConfigMixin, ExecutionStrategy
from at_em_imaging_workflow.render_strategy_utils import RenderStrategyUtils
from rendermodules.pointmatch.schemas import PointMatchClientParametersSpark
from workflow_engine.models import WellKnownFile
import jinja2
import os
from django.conf import settings
import logging


class TwoDMontagePointMatchStrategy(InputConfigMixin, ExecutionStrategy):
    _package = (
        'at_em_imaging_workflow.strategies.'
        'montage.two_d_montage_point_match_strategy')
    _templates = 'templates'
    _log_configuration_template = 'spark_log4j_template.properties'
    _log = logging.getLogger(_package)

    def get_input(self, em_mset, storage_directory, task):
        inp = self.get_workflow_node_input_template(
            task,
            name='2D Montage Point Match Input')

        inp['render'] = RenderStrategyUtils.render_input_dict(em_mset)

        inp['sparkhome'] = settings.SPARK_HOME
        log_dir = self.get_or_create_task_storage_directory(task)
        inp['logdir'] = log_dir


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

        redo_cfg = em_mset.get_redo_parameters()
        
        if ('render_scale' in redo_cfg and
            redo_cfg['render_scale'] is not None):
            inp['renderScale'] = redo_cfg['render_scale']

        return PointMatchClientParametersSpark().dump(inp).data

    def get_tile_pairs_file_name(self, em_mset):
        return WellKnownFile.get(
            em_mset,
            em_mset.tile_pairs_file_description())


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
