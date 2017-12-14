from workflow_engine.strategies import execution_strategy
from django.conf import settings
from development.strategies.schemas.generate_mip_maps import input_dict
from rendermodules.dataimport.schemas import AddMipMapsToStackParameters
import logging


class ApplyMipMapsStrategy(execution_strategy.ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.apply_mip_maps_strategy')
    
    def get_input(self, em_mset, storage_directory, task):
        ApplyMipMapsStrategy._log.info('get_input')
        inp = input_dict
        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = settings.RENDER_SERVICE_PROJECT
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['input_stack'] = self.get_input_stack_name()
        inp['mipmap_dir'] = em_mset.mipmap_directory
        inp['output_dir'] = self.get_or_create_task_storage_directory(task)

        inp['zstart'] = em_mset.section.z_index
        inp['zend'] = em_mset.section.z_index

        return AddMipMapsToStackParameters().dump(inp).data


    def get_input_stack_name(self):
        return settings.RENDER_STACK_NAME


    def on_finishing(self, enqueued_object, results, task):
        # self.check_key(results, 'output_json')
        # self.set_well_known_file(results['output_json'], enqueued_object, 'description', task)
        pass

    #override if needed
    #set the storage directory for an enqueued object
    #def get_storage_directory(self, base_storage_directory, job):
    #  enqueued_object = job.get_enqueued_object()
    #  return os.path.join(base_storage_directory, 'reference_set_' + str(enqueued_object.id))
