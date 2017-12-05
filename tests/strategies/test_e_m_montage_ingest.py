import pytest
from development.strategies.lens_correction_ingest import LensCorrectionIngest
from development.models.e_m_montage_set import EMMontageSet
from rendermodules.ingest.schemas import example as body_data
import copy


@pytest.mark.django_db
@pytest.mark.skipif(True, reason='moved all to lens correction ingest')
def test_with_reference_set():
    ref_body_data = None
    example = body_data

    example['manifest_path'] = \
        "/allen/aibs/pipeline/image_processing/volume_assembly/" + \
        "lc_test_data/Wij_Set_594451332/594089217_594451332/" + \
        "_trackem_20170502174048_295434_5LC_0064_" + \
        "01_20170502174047_reference_0_.txt"
    example['storage_directory'] = \
        "/allen/aibs/pipeline/image_processing/volume_assembly/" + \
        "lc_test_data/Wij_Set_594451332/594089217_594451332"
    example['metafile'] = \
        "/allen/aibs/pipeline/image_processing/volume_assembly/" + \
        "dataimport_test_data/" + \
        "_metadata_20170829130146_295434_5LC_0064_01_redo_001050_0_.json"

    ref_set = LensCorrectionIngest().create_reference_set(example)
    em_mset = LensCorrectionIngest().create_em_montage_set(example)

    assert ref_set is not None
    assert em_mset is not None

    get_em_mset = EMMontageSet.objects.get(
        storage_directory=example['storage_directory'])

    assert get_em_mset is not None
    assert body_data['reference_set_id'] == em_mset.reference_set.uid
    assert body_data['acquisition_data']['overlap'] == em_mset.overlap
    assert body_data['storage_directory'] == em_mset.storage_directory
    assert body_data['section']['z_index'] == em_mset.section.z_index
    #assert example['acquisition_data']['microscope'] == \
    #    ref_set.microscope.microscope_type.name
    #assert example['acquisition_data']['camera']['camera_id'] == \
    #    ref_set.camera.uid
    #assert example['acquisition_data']['camera']['height'] == \
    #    ref_set.camera.height
    #assert example['acquisition_data']['camera']['width'] == \
    #    ref_set.camera.width
    #assert example['acquisition_data']['camera']['model'] == \
    #    ref_set.camera.model
    assert example['acquisition_data']['acquisition_time'] == \
        em_mset.acquisition_date


@pytest.fixture
def em_mset_no_ref_set():
    example = copy.deepcopy(body_data)

    del example['reference_set_id']
    example['manifest_path'] = \
        "/allen/aibs/pipeline/image_processing/volume_assembly/" + \
        "lc_test_data/Wij_Set_594451332/594089217_594451332/" + \
        "_trackem_20170502174048_295434_5LC_0064_" + \
        "01_20170502174047_reference_0_.txt"
    example['storage_directory'] = \
        "/allen/aibs/pipeline/image_processing/volume_assembly/" + \
        "lc_test_data/Wij_Set_594451332/594089217_594451332"
    example['metafile'] = \
        "/allen/aibs/pipeline/image_processing/volume_assembly/" + \
        "dataimport_test_data/" + \
        "_metadata_20170829130146_295434_5LC_0064_01_redo_001050_0_.json"

    return example


@pytest.mark.django_db
def test_em_mset_camera(em_mset_no_ref_set):
    em_mset = LensCorrectionIngest().create_em_montage_set(em_mset_no_ref_set)

    assert em_mset_no_ref_set['acquisition_data']['camera']['camera_id'] == \
        em_mset.camera.uid
    assert em_mset_no_ref_set['acquisition_data']['camera']['height'] == \
        em_mset.camera.height
    assert em_mset_no_ref_set['acquisition_data']['camera']['width'] == \
        em_mset.camera.width
    assert em_mset_no_ref_set['acquisition_data']['camera']['model'] == \
        em_mset.camera.model


@pytest.mark.django_db
def test_mset_microscope(em_mset_no_ref_set):
    em_mset = LensCorrectionIngest().create_em_montage_set(em_mset_no_ref_set)

    assert em_mset_no_ref_set['acquisition_data']['microscope'] == \
        em_mset.microscope.microscope_type.name


@pytest.mark.django_db
def test_mset_section(em_mset_no_ref_set):
    em_mset = LensCorrectionIngest().create_em_montage_set(em_mset_no_ref_set)

    assert body_data['section']['z_index'] == em_mset.section.z_index


@pytest.mark.django_db
def test_mset_storage_directory(em_mset_no_ref_set):
    em_mset = LensCorrectionIngest().create_em_montage_set(em_mset_no_ref_set)

    assert em_mset_no_ref_set['storage_directory'] == em_mset.storage_directory


@pytest.mark.django_db
@pytest.mark.xfail
def test_mset_mipmap_directory(em_mset_no_ref_set):
    em_mset = LensCorrectionIngest().create_em_montage_set(em_mset_no_ref_set)

    assert em_mset.mipmap_directory is not None


@pytest.mark.django_db
def test_mset_metafile(em_mset_no_ref_set):
    em_mset = LensCorrectionIngest().create_em_montage_set(em_mset_no_ref_set)

    assert em_mset_no_ref_set['metafile'] == em_mset.metafile

@pytest.mark.django_db
def test_without_reference_set(em_mset_no_ref_set):
    em_mset = LensCorrectionIngest().create_em_montage_set(em_mset_no_ref_set)

    assert em_mset is not None

    get_em_mset = EMMontageSet.objects.get(
        storage_directory=em_mset_no_ref_set['storage_directory'])

    assert get_em_mset is not None
    assert em_mset.reference_set is None
    assert em_mset.reference_set_uid is None
    assert body_data['acquisition_data']['overlap'] == em_mset.overlap
    assert em_mset_no_ref_set['storage_directory'] == em_mset.storage_directory
    assert em_mset_no_ref_set['acquisition_data']['acquisition_time'] == \
        em_mset.acquisition_date

