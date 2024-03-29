import pytest
from workflow_engine.models import (
    Configuration,
    Task,
    Job,
    JobQueue,
    WorkflowNode
)
from tests.fixtures.model_fixtures import (
    cameras_etc,           # noqa # pylint: disable=unused-import
    section_factory,       # noqa # pylint: disable=unused-import
    lots_of_montage_sets,  # noqa # pylint: disable=unused-import
    lots_of_chunks         # noqa # pylint: disable=unused-import
)
from django.test.utils import override_settings


@pytest.mark.render_schema_failure
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
    from at_em_imaging_workflow.strategies.rough.apply_rough_alignment_strategy \
        import ApplyRoughAlignmentStrategy

    chnk = lots_of_chunks[2]
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

    assert inp['render'] == {
        "host": "MOCK_URL",
        "project": "MOCK SPECIMEN",
        "owner": "MOCK_USER",
        "port": 9999,
        "memGB": "5G",
        "client_scripts": "/path/to/mock/client/scripts"
    }

    assert inp['old_z'] == list(range(10180,10280 + 1))
    assert inp['new_z'] == list(range(180, 280 + 1))

    assert inp['montage_stack'] == 'em_2d_montage_solved_py'
    assert inp['prealigned_stack'] == 'em_2d_montage_solved_py'

    assert inp['lowres_stack'] == 'em_rough_align_solved_downsample_zs180_ze280'
    assert inp['output_stack'] == 'em_rough_align_zs180_ze280'
