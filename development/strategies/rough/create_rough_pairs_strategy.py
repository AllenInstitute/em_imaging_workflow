from workflow_engine.strategies.execution_strategy import ExecutionStrategy
from development.models.chunk_assignment import ChunkAssignment
from development.strategies.rough.solve_rough_alignment_strategy \
    import SolveRoughAlignmentStrategy
from rendermodules.pointmatch.schemas import \
    TilePairClientParameters
from django.conf import settings
import logging
from development.strategies import get_workflow_node_input_template
from at_em_imaging_workflow.two_d_stack_name_manager \
    import TwoDStackNameManager


class CreateRoughPairsStrategy(ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.create_rough_pairs_strategy')

    #
    # Don't get anything for now.  Stop processing.
    # Todo: check if all sections are in a good state
    # then return the chunk object
    def get_objects_for_queue(self, prev_queue_job):
        objects = []
        # objects.append(prev_queue_job.get_enqueued_object())
        return objects

    def get_input(self, chk_assgn, storage_directory, task):
        inp = get_workflow_node_input_template(task)

        chnk = chk_assgn.chunk

        stack_names = \
            TwoDStackNameManager.create_rough_pair_stacks(
                chk_assgn)

        inp['render']['host'] = settings.RENDER_SERVICE_URL
        inp['render']['port'] = settings.RENDER_SERVICE_PORT
        inp['render']['owner'] = settings.RENDER_SERVICE_USER
        inp['render']['project'] = chnk.get_render_project_name()
        inp['render']['client_scripts'] = settings.RENDER_CLIENT_SCRIPTS

        inp['output_dir'] = chnk.get_storage_directory()

        tile_pair_ranges = \
            SolveRoughAlignmentStrategy.get_tile_pair_ranges(chnk)

        section_z_index = chk_assgn.section.z_index

        for k in tile_pair_ranges.keys():
            tile_pair_range = tile_pair_ranges[k]
            if tile_pair_range['tempz'] == section_z_index:
                min_z = tile_pair_range['minz']
                max_z = tile_pair_range['maxz']

                inp["minZ"] = min_z
                inp["maxZ"] = max_z
                inp["zNeighborDistance"] = tile_pair_range["zNeighborDistance"]

        inp['baseStack'] = stack_names['baseStack']
        inp['stack'] = stack_names['stack']

        return TilePairClientParameters().dump(inp).data

    def on_finishing(self, chk_assgn, results, task):
        chnk = chk_assgn.chunk
        z_index = str(chk_assgn.section.z_index)

        self.check_key(results, 'tile_pair_file')

        cfg, created = chnk.configurations.get_or_create(
            configuration_type='rough_tile_pair_file')

        if created:
            cfg.json_object = {
                z_index: {
                    'tile_pair_file': results['tile_pair_file']
                }
            }
        else:
            cfg.json_object[z_index] = {
                'tile_pair_file': results['tile_pair_file']
            }
        cfg.save()

    def get_task_objects_for_queue(self, chnk):
        tile_pair_ranges = \
            SolveRoughAlignmentStrategy.get_tile_pair_ranges(chnk)

        chunk_assignments = [
            ChunkAssignment.objects.get(
                chunk=chnk,
                section__z_index=tile_pair_ranges[x]['tempz']
            ) for x in tile_pair_ranges.keys()]

        return chunk_assignments

    def get_storage_directory(self, base_storage_directory, job):
        chnk = job.get_enqueued_object()

        return chnk.get_storage_directory(
            base_storage_directory)

