from at_em_imaging_workflow.strategies.montage.make_montage_scapes_stack_strategy \
    import MakeMontageScapesStackStrategy
from at_em_imaging_workflow.models import EMMontageSet
from tests.strategies.at_em_fixtures import (
    strategy_configurations  # noqa # pylint: disable=unused-import
)
import pytest
from mock import Mock, patch
from workflow_engine.models import Configuration, Task
from tests.models.test_chunk_model import (
    cameras_etc,          # noqa # pylint: disable=unused-import
    section_factory,      # noqa # pylint: disable=unused-import
    lots_of_montage_sets  # noqa # pylint: disable=unused-import
)
from tests.strategies.rough.test_rough_point_match_strategy import (
    lots_of_chunks  # noqa # pylint: disable=unused-import
)


@pytest.mark.django_db
@patch('at_em_imaging_workflow.strategies.montage.'
       'make_montage_scapes_stack_strategy.MakeMontageScapesStackStrategy.'
       'get_workflow_node_input_template',
       Mock(return_value={
           'montage_stack': "",
           'output_stack': "",
           'render': { } } ))
def test_get_input_data(
    lots_of_chunks,
    strategy_configurations
):
    chnk = lots_of_chunks[0]
    min_z = min(int(i) for i in chnk.get_z_mapping().keys())
    chnk_assign = chnk.chunkassignment_set.get(
        section__z_index=min_z
    )

    strategy = MakeMontageScapesStackStrategy()
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

    assert inp['set_new_z'] == True
    assert inp['minZ'] == 10000
    assert inp['maxZ'] == 10000
    assert inp['new_z_start'] == 0

    assert inp['image_directory'] == \
        '/long/term/em_montage_set/MOCK SPECIMEN_z10000_2345_06_07_16_09_09_00_00'

    assert inp['montage_stack'] == 'em_2d_montage_solved_py'
    assert inp['output_stack'] == 'em_2d_montage_solved_py_0_01_mapped'

    assert inp['render']['host'] == 'renderservice'
    assert inp['render']['port'] == 8080
    assert inp['render']['owner'] == 'test_user'
    assert inp['render']['project'] == 'MOCK SPECIMEN'
    assert inp['render']['client_scripts'].startswith('/allen/aibs')


@pytest.mark.django_db
def test_get_one_task_objects_for_queue(lots_of_chunks):
    chnk = lots_of_chunks[0]
    min_z = min(int(i) for i in chnk.get_z_mapping().keys())
    chnk_assign = chnk.chunkassignment_set.get(
        section__z_index=min_z
    )
    em_mset = chnk_assign.section.montageset_set.get().emmontageset

    strategy = MakeMontageScapesStackStrategy()
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
    em_mset = EMMontageSet.objects.filter(
        section=chnk_assign.section)[0]
    strategy = MakeMontageScapesStackStrategy()

    tsks = strategy.get_task_objects_for_queue(em_mset)

    assert tsks is not None
    assert len(tsks) == 1

