import pytest
from workflow_engine.models import (
    Configuration,
    Task,
    Job,
    JobQueue,
    WorkflowNode
)
from at_em_imaging_workflow.strategies.rough.apply_rough_alignment_strategy \
    import ApplyRoughAlignmentStrategy
from tests.fixtures.model_fixtures import (
    cameras_etc,
    section_factory,
    lots_of_montage_sets,
    lots_of_chunks
)
from django.test.utils import override_settings
from mock import Mock, patch


@pytest.mark.django_db
@override_settings(
    RENDER_SERVICE_URL='MOCK_URL',
    RENDER_SERVICE_PORT=9999,
    RENDER_SERVICE_USER='MOCK_USER',
    RENDER_CLIENT_SCRIPTS='/path/to/mock/client/scripts',
    CHUNK_DEFAULTS={
        'overlap': 2,
        'start_z': 1,
        'chunk_size': 5 })
def test_get_input_data(lots_of_chunks):
    chnk = lots_of_chunks[2]
#     z_map = Configuration(
#         name='Z',
#         configuration_type="z_mapping",
#         json_object={ str(k+1000): k for k in range(17,27) }
#     )
#     chnk.configurations.add(z_map, bulk=False)

    jq = JobQueue(name="Apply Rough Alignment")
    input_con = Configuration(
        name="Apply Rough Alignment Input",
        configuration_type="strategy_config",
        json_object={})

    wn = WorkflowNode(job_queue=jq)
    wn.configurations.add(input_con, bulk=False)
    jb = Job(workflow_node=wn)
    task = Task(id=345, job=jb)

    storage_directory = '/example/storage/directory'
    strategy = ApplyRoughAlignmentStrategy()
    inp = strategy.get_input(
        chnk,
        storage_directory,
        task)

    assert inp['render']['project'] == 'MOCK SPECIMEN'
    assert inp['render']['owner'] == 'MOCK_USER'
    assert inp['render']['port'] == 9999
    assert inp['render']['host'] == 'MOCK_URL'
    assert inp['render']['client_scripts'] == '/path/to/mock/client/scripts'

    assert inp['old_z'] == list(range(10180,10280 + 1))
    assert inp['new_z'] == list(range(180, 280 + 1))

    assert inp['montage_stack'] == 'em_2d_montage_solved_py'
    assert inp['prealigned_stack'] == 'em_2d_montage_solved_py'
    assert inp['lowres_stack'] == 'em_rough_align_solved_downsample_zs180_ze280'
    assert inp['output_stack'] == 'em_rough_align_zs180_ze280'

