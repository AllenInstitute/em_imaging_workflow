from at_em_imaging_workflow.strategies.montage.remap_z_strategy import RemapZStrategy
from at_em_imaging_workflow.models.chunk_assignment import ChunkAssignment
from at_em_imaging_workflow.models.e_m_montage_set import EMMontageSet
from workflow_engine.models.configuration import Configuration
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
def test_get_input_data(lots_of_chunks):
    chnk = lots_of_chunks[0]
    min_z = min(int(i) for i in chnk.get_z_mapping().keys())
    chnk_assign = chnk.chunkassignment_set.get(
        section__z_index=min_z
    )

    storage_directory = '/example/storage/directory'
    em_mset = EMMontageSet.objects.filter(
        section=chnk_assign.section).first()
    task = Mock()#Task(id=345, enqueued_task_object=em_mset)

    downsample_config = Configuration(
        content_object=em_mset,
        name='%s downsample temp_stack' % str(em_mset),
        configuration_type='downsample temp stack',
        json_object={ 
            'downsample_temp_stack' : 'mock_stack'
        })
    downsample_config.save()

    with patch('at_em_imaging_workflow.strategies.montage.'
               'remap_z_strategy.RemapZStrategy.'
               'get_workflow_node_input_template',
               Mock(return_value={
                   'montage_stack': "",
                   'output_stack': "",
                   'render': { } } )):
        strategy = RemapZStrategy()
        inp = strategy.get_input(
            em_mset,
            storage_directory,
            task)

    assert inp['zValues'] == [10000]
    assert inp['new_zValues'] == [0]

    assert inp['input_stack'] == 'em_2d_montage_downsampled_no_mapping'
    assert inp['output_stack'] == 'em_2d_montage_solved_py_0_01_mapped'

    assert inp['render']['host'] == 'renderservice'
    assert inp['render']['port'] == 8080
    assert inp['render']['owner'] == 'test_user'
    assert inp['render']['project'] == 'MOCK SPECIMEN'
    assert inp['render']['client_scripts'].startswith('/allen/aibs')

    # assert json.dumps(inp, indent=2) == ''


@pytest.mark.django_db
def test_get_one_task_objects_for_queue(lots_of_chunks):
    chnk = lots_of_chunks[0]
    min_z = min(int(i) for i in chnk.get_z_mapping().keys())
    chnk_assign = chnk.chunkassignment_set.get(
        section__z_index=min_z
    )
    em_mset = chnk_assign.section.montageset_set.get().emmontageset
    strategy = RemapZStrategy()

    tsks = strategy.get_task_objects_for_queue(em_mset)

    assert tsks is not None
    assert len(tsks) == 1


@pytest.mark.django_db
def test_get_two_task_objects_for_queue(lots_of_chunks):
    chnk = lots_of_chunks[0]
    max_z = max(int(i) for i in chnk.get_z_mapping().keys())
    chnk_assign = chnk.chunkassignment_set.get(
        section__z_index=max_z
    )
    em_mset = chnk_assign.section.montageset_set.get().emmontageset
    strategy = RemapZStrategy()

    tsks = strategy.get_task_objects_for_queue(em_mset)

    assert tsks is not None
    assert len(tsks) == 1

