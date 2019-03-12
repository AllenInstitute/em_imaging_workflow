from development.strategies.rough.remap_z_strategy import RemapZStrategy
from development.models.chunk_assignment import ChunkAssignment
from development.models.e_m_montage_set import EMMontageSet
from workflow_engine.models.configuration import Configuration
from tests.strategies.at_em_fixtures import strategy_configurations
import pytest
from mock import Mock, patch, mock_open
from workflow_engine.models.task import Task
from workflow_engine.models.job import Job
from django.test.utils import override_settings
from tests.models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from tests.strategies.rough.test_rough_point_match_strategy \
    import lots_of_chunks
# import simplejson as json


@pytest.mark.django_db
@patch('development.strategies.rough'
       '.remap_z_strategy'
       '.get_workflow_node_input_template',
       Mock(return_value={
           'montage_stack': "",
           'output_stack': "",
           'render': { } } ))
def test_get_input_data(lots_of_chunks,
                        strategy_configurations):
    chnk_assigns = ChunkAssignment.objects.filter(
        chunk=lots_of_chunks[0])
    chnk_assign = chnk_assigns[0]
    strategy = RemapZStrategy()
    storage_directory = '/example/storage/directory'
    task = Task(id=345)

    em_mset = EMMontageSet.objects.filter(
        section=chnk_assign.section).first()

    downsample_config = Configuration(
        content_object=em_mset,
        name='%s downsample temp_stack' % str(em_mset),
        configuration_type='downsample temp stack',
        json_object={ 
            'downsample_temp_stack' : 'mock_stack'
        })
    downsample_config.save()

    inp = strategy.get_input(
        em_mset,
        storage_directory,
        task)

    assert inp['zValues'] == [2]
    assert inp['new_zValues'] == [1]

    assert inp['input_stack'] == 'em_2d_montage_solved_py_0_01_mapped'
    assert inp['output_stack'] == 'em_2d_montage_downsampled_no_mapping'

    assert inp['render']['host'] == 'renderservice'
    assert inp['render']['port'] == 8080
    assert inp['render']['owner'] == 'test_user'
    assert inp['render']['project'] == 'MOCK SPECIMEN'
    assert inp['render']['client_scripts'].startswith('/allen/aibs')

    # assert json.dumps(inp, indent=2) == ''


@pytest.mark.django_db
def test_get_one_task_objects_for_queue(lots_of_chunks):
    chnk_assigns = ChunkAssignment.objects.filter(
        section__z_index=1)
    chnk_assign = chnk_assigns[0]
    em_mset = EMMontageSet.objects.filter(
        section=chnk_assign.section)[0]
    strategy = RemapZStrategy()

    tsks = strategy.get_task_objects_for_queue(em_mset)

    assert tsks is not None
    assert len(tsks) == 1


@pytest.mark.django_db
def test_get_two_task_objects_for_queue(lots_of_chunks):
    chnk_assigns = ChunkAssignment.objects.filter(
        section__z_index=10)
    chnk_assign = chnk_assigns[0]
    em_mset = EMMontageSet.objects.filter(
        section=chnk_assign.section)[0]
    strategy = RemapZStrategy()

    tsks = strategy.get_task_objects_for_queue(em_mset)

    assert tsks is not None
    assert len(tsks) == 1

