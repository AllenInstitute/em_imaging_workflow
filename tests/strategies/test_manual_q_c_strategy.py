from mock import Mock, patch
from development.strategies import RENDER_STACK_INGEST, RENDER_STACK_SOLVED,\
    RENDER_STACK_LENS_CORRECTED
import pytest
from workflow_engine.models.task import Task
from development.strategies.manual_q_c_strategy \
    import ManualQCStrategy
from django.test.utils import override_settings
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets


@override_settings(
    RENDER_SERVICE_URL='MOCK_URL',
    RENDER_SERVICE_PORT=9999,
    RENDER_SERVICE_USER='MOCK_USER',
    RENDER_CLIENT_SCRIPTS='/path/to/mock/client/scripts',
)
def test_get_input_data():
    em_mset = Mock()
    em_mset.get_point_collection_name = Mock(
        return_value='MOCK_COLLECTION')
    em_mset.get_render_project_name = Mock(
        return_value='MOCKSPECIMEN')
    em_mset.section = Mock()
    em_mset.section.specimen = Mock()
    em_mset.section.specimen.uid = \
        'MOCKSPECIMEN'
    em_mset.section.z_index = 1515
    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = ManualQCStrategy()

    inp = strategy.get_input(em_mset,
                             storage_directory,
                             task)

    assert inp['render']['project'] == 'MOCKSPECIMEN'
    assert inp['render']['owner'] == 'MOCK_USER'
    assert inp['render']['port'] == 9999
    assert inp['render']['host'] == 'MOCK_URL'
    assert inp['render']['client_scripts'] == '/path/to/mock/client/scripts'
    assert inp['prestitched_stack'] == RENDER_STACK_LENS_CORRECTED
    assert inp['poststitched_stack'] == RENDER_STACK_SOLVED
    assert inp['match_collection'] == 'MOCK_COLLECTION'
    assert inp['minZ'] == 1515
    assert inp['maxZ'] == 1515


@pytest.mark.django_db
@patch('shutil.copy')
@patch('os.makedirs')
@patch('os.path.exists')
def test_on_finishing_passed(
    shcpy, mkmock, existmock,
        lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    em_mset.section.z_index = 222
    results = { 'qc_passed_sections': [222],
                'gap_sections': [],
                'seam_sections': [],
                'hole_sections': [] }
    task = Mock()

    strategy = ManualQCStrategy()
    strategy.set_well_known_file = Mock()
    strategy.on_finishing(em_mset, results, task)

    assert em_mset.workflow_state == 'MONTAGE_QC_PASSED'
    strategy.set_well_known_file.assert_called_once()


@pytest.mark.django_db
@patch('shutil.copy')
@patch('os.makedirs')
@patch('os.path.exists')
def test_on_finishing_gap(
    shcpy, mkmock, existmock,
        lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    em_mset.section.z_index = 222
    results = { 'qc_passed_sections': [],
                'gap_sections': [222],
                'seam_sections': [],
                'hole_sections': [] }
    task = Mock()

    strategy = ManualQCStrategy()
    strategy.set_well_known_file = Mock()
    strategy.on_finishing(em_mset, results, task)

    assert em_mset.workflow_state == 'MONTAGE_QC_FAILED'
    strategy.set_well_known_file.assert_called_once()


@pytest.mark.django_db
@patch('shutil.copy')
@patch('os.makedirs')
@patch('os.path.exists')
def test_on_finishing_seam(
    shcpy, mkmock, existmock,
        lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    em_mset.section.z_index = 222
    results = { 'qc_passed_sections': [],
                'gap_sections': [],
                'seam_sections': [222],
                'hole_sections': [] }
    task = Mock()

    strategy = ManualQCStrategy()
    strategy.set_well_known_file = Mock()
    strategy.on_finishing(em_mset, results, task)

    assert em_mset.workflow_state == 'MONTAGE_QC_FAILED'
    strategy.set_well_known_file.assert_called_once()


@pytest.mark.django_db
@patch('shutil.copy')
@patch('os.makedirs')
@patch('os.path.exists')
def test_on_finishing_hole(
    shcpy, mkmock, existmock,
        lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    em_mset.section.z_index = 222
    results = { 'qc_passed_sections': [],
                'gap_sections': [],
                'seam_sections': [],
                'hole_sections': [222] }
    task = Mock()

    strategy = ManualQCStrategy()
    strategy.set_well_known_file = Mock()
    strategy.on_finishing(em_mset, results, task)

    assert em_mset.workflow_state == 'MONTAGE_QC_FAILED'
    strategy.set_well_known_file.assert_called_once()