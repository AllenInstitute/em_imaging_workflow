from django_fsm import can_proceed
from workflow_engine.strategies import WaitStrategy
from at_em_imaging_workflow.models import EMMontageSet, Load
import logging

class LoadZMappingStrategy(WaitStrategy):
    _log = logging.getLogger(
        'at_em_imaging_workflow.strategies.montage.'
        'load_z_mapping'
    )

    def can_transition(self, load, source_node=None):
        if load.object_state == Load.STATE.LOAD_PENDING:
            return True

        return False

    def transform_objects_for_queue(self, source_object):
        if type(source_object) is EMMontageSet:
            em_mset = source_object
            load = em_mset.sample_holder.load

            return [load]
        elif type(source_object) is Load:
            load = source_object

            return [load]
        else:
            return []

    def must_wait(self, load):
        if load.configurations.filter(
            configuration_type='z_mapping'
        ).count() > 0:
            LoadZMappingStrategy._log.info('has z mapping')
            if can_proceed(load.z_mapped):
                load.z_mapped()
                LoadZMappingStrategy._log.info(
                    'changing state'
                )
            else:
                LoadZMappingStrategy._log.warn(
                    'Load was not in pending.'
                )
                load.object_state = Load.STATE.LOAD_Z_MAPPED
            load.save()

            return False

        return True