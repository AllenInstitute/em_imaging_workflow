import os
import simplejson as json
from development.strategies.rough.make_montage_scapes_stack_strategy import MakeMontageScapesStackStrategy
from development.models.chunk_assignment import ChunkAssignment
from development.models.e_m_montage_set import EMMontageSet
os.environ['BLUE_SKY_SETTINGS'] = '/local1/git/at_em_imaging_workflow/at_em_imaging_workflow/blue_sky_settings.yml'

import pytest
from mock import Mock, patch, mock_open
from workflow_engine.models.task import Task
from workflow_engine.models.job import Job
from django.test.utils import override_settings
from workflow_engine.workflow_controller import WorkflowController
from development.models.chunk import Chunk
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from strategies.rough.test_rough_point_match_strategy \
    import lots_of_chunks


@pytest.mark.django_db
def test_get_input_data(lots_of_chunks):
    chnk_assigns = ChunkAssignment.objects.filter(
        chunk=lots_of_chunks[0])
    chnk_assign = chnk_assigns[0]
    strategy = MakeMontageScapesStackStrategy()
    storage_directory = '/example/storage/directory'
    task = Task(id=345)
    inp = strategy.get_input(
        chnk_assign,
        storage_directory,
        task)

    assert inp['minZ'] == 1
    assert inp['maxZ'] == 10

    assert inp['image_directory'] == '/example/storage/directory'

    assert inp['montage_stack'] == 'em_2d_montage_solved'
    assert inp['output_stack'] == 'em_rough_align_scapes_zs_1_ze_10'

    assert inp['render']['host'] == 'renderservice'
    assert inp['render']['port'] == 8080
    assert inp['render']['owner'] == 'test_user'
    assert inp['render']['project'] == 'MOCK SPECIMEN'
    assert inp['render']['client_scripts'].startswith('/allen/aibs')

    # assert json.dumps(inp, indent=2) == ''


@pytest.mark.django_db
def test_get__one_task_objects_for_queue(lots_of_chunks):
    chnk_assigns = ChunkAssignment.objects.filter(
        section__z_index=1)
    chnk_assign = chnk_assigns[0]
    em_mset = EMMontageSet.objects.filter(
        section=chnk_assign.section)[0]
    strategy = MakeMontageScapesStackStrategy()

    tsks = strategy.get_task_objects_for_queue(em_mset)

    assert tsks is not None
    assert len(tsks) == 1


@pytest.mark.django_db
def test_get__two_task_objects_for_queue(lots_of_chunks):
    chnk_assigns = ChunkAssignment.objects.filter(
        section__z_index=10)
    chnk_assign = chnk_assigns[0]
    em_mset = EMMontageSet.objects.filter(
        section=chnk_assign.section)[0]
    strategy = MakeMontageScapesStackStrategy()

    tsks = strategy.get_task_objects_for_queue(em_mset)

    assert tsks is not None
    assert len(tsks) == 2

