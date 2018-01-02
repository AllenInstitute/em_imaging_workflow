from workflow_engine.strategies.execution_strategy import \
    ExecutionStrategy
from rendermodules.pointmatch.schemas import \
    PointMatchClientParametersSpark
import copy
from workflow_engine.models.well_known_file import WellKnownFile
from development.strategies.schemas.two_d_montage_point_match \
    import input_dict
from django.conf import settings
import logging

class TwoDMontagePointMatchStrategy(ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.two_d_montage_point_match_strategy')

    def get_input(self, em_mset, storage_directory, task):
        TwoDMontagePointMatchStrategy._log.info("get input")

        inp = copy.deepcopy(input_dict)

        inp['sparkhome'] = settings.SPARK_HOME
        inp['logdir'] = self.get_or_create_task_storage_directory(task)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['owner'] = settings.RENDER_SERVICE_USER

        inp['jarfile'] = settings.RENDER_SPARK_JARFILE

        inp['collection'] = self.get_collection_name()
        inp['pairJson'] = self.get_tile_pairs_file_name(em_mset)

        mem = 128
        ppn = 24
        inp['memory'] = str(int((mem - ppn) / ppn)) + 'g'
        inp['driverMemory'] = str(int(mem)) +  'g'  # TODO roughly memory * ppn

        inp['masterUrl'] = 'local[*]'
        inp['baseDataUrl'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ':' + settings.RENDER_SERVICE_PORT + '/render-ws/v1'

        return PointMatchClientParametersSpark().dump(inp).data

    def get_tile_pairs_file_name(self, em_mset):
        return WellKnownFile.get(
            em_mset,
            em_mset.tile_pairs_file_description())

    def get_collection_name(self):
        return 'default_point_matches'
        # return settings.POINT_MATCH_COLLECTION_NAME

    def on_finishing(self, em_mset, results, task):
        self.check_key(results, 'pairCount')
        self.set_well_known_file(
            self.get_output_file(task),
            em_mset,
            'point_match_output',
            task)

