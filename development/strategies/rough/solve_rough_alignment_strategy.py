from workflow_engine.strategies.execution_strategy \
    import ExecutionStrategy
from rendermodules.rough_align.schemas \
    import SolveRoughAlignmentParameters
import copy
from development.models.e_m_montage_set import EMMontageSet
from development.strategies \
    import RENDER_STACK_DOWNSAMPLED, RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE, \
    get_workflow_node_input_template
from django.conf import settings


class SolveRoughAlignmentStrategy(ExecutionStrategy):

    @classmethod
    def get_load(cls, chnk):
        chunk_section = chnk.sections.first()
        load_mset = EMMontageSet.objects.filter(
            section=chunk_section).last()

        return load_mset.sample_holder.load

    @classmethod
    def get_z_mapping(cls, load):
        return copy.deepcopy(
            load.configurations.get(
                configuration_type='z_mapping').json_object)

    @classmethod
    def calculate_z_min_max(cls, tile_pair_ranges):
        min_z = min([rng['minz'] for rng in tile_pair_ranges.values()])
        max_z = max([rng['maxz'] for rng in tile_pair_ranges.values()])

        return min_z,max_z

    @classmethod
    def clip_z_mapping_to_min_max(cls, z_mapping, min_z, max_z):
        clipped_mapping = {
            k: v for k,v in z_mapping.items() if v >= min_z and v <= max_z
        }

        return clipped_mapping

    @classmethod
    def get_tile_pair_ranges(cls, chnk):
        tile_pair_config= chnk.configurations.get(
            configuration_type='chunk_configuration').json_object

        return tile_pair_config['tile_pair_ranges']

    def get_input(self, chnk, storage_directory, task):
        inp = get_workflow_node_input_template(
            task,
            name='Rough Alignment Solver Input')

        chunk_load = \
            SolveRoughAlignmentStrategy.get_load(chnk)
        z_mapping = \
            SolveRoughAlignmentStrategy.get_z_mapping(chunk_load)
        tile_pair_ranges = \
            SolveRoughAlignmentStrategy.get_tile_pair_ranges(chnk)
        min_z, max_z = \
            SolveRoughAlignmentStrategy.calculate_z_min_max(tile_pair_ranges)
        clipped_z_mapping = \
            SolveRoughAlignmentStrategy.clip_z_mapping_to_min_max(
                z_mapping, min_z, max_z)

        zs = [int(z) for z in clipped_z_mapping.values()]
        z_start = min(zs)
        z_end = max(zs)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['source_collection']['service_host'] = \
            settings.RENDER_SERVICE_URL + ":" + str(settings.RENDER_SERVICE_PORT)
        inp['source_collection']['baseURL'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + str(settings.RENDER_SERVICE_PORT) + '/render-ws/v1'
        inp['source_collection']['owner'] = settings.RENDER_SERVICE_USER
        inp['source_collection']['project'] = chnk.get_render_project_name()
        inp['source_collection']['renderbinPath'] = \
            settings.RENDER_CLIENT_SCRIPTS

        if inp['source_collection']['stack'] == '':
            inp['source_collection']['stack'] = \
                RENDER_STACK_DOWNSAMPLED

        inp['target_collection']['service_host'] = \
            settings.RENDER_SERVICE_URL + ":" + str(settings.RENDER_SERVICE_PORT)
        inp['target_collection']['baseURL'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + str(settings.RENDER_SERVICE_PORT) + '/render-ws/v1'
        inp['target_collection']['owner'] = settings.RENDER_SERVICE_USER
        inp['target_collection']['project'] = chnk.get_render_project_name()
        inp['target_collection']['renderbinPath'] = \
            settings.RENDER_CLIENT_SCRIPTS

        if inp['target_collection']['stack'] == '':
            inp['target_collection']['stack'] = \
                RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE % (z_start, z_end)

        inp['source_point_match_collection']['server'] = \
            'http://' + settings.RENDER_SERVICE_URL + \
            ":" + str(settings.RENDER_SERVICE_PORT) + '/render-ws/v1'
        inp['source_point_match_collection']['owner'] = \
            settings.RENDER_SERVICE_USER
        if inp['source_point_match_collection']['match_collection'] == '':
            inp['source_point_match_collection']['match_collection'] = \
                chnk.get_point_collection_name()

        inp['first_section'] = z_start
        inp['last_section'] = z_end

        inp['solver_options']['dir_scratch'] = storage_directory
        inp['solver_executable'] = settings.MONTAGE_SOLVER_BIN

        return SolveRoughAlignmentParameters().dump(inp).data
