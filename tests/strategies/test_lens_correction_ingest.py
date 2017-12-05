#from django.utils import dateparse
#import os
#import pytz
import pytest
from mock import patch, Mock
from development.strategies.lens_correction_ingest import LensCorrectionIngest
from development.models.reference_set import ReferenceSet
from development.models.e_m_montage_set import EMMontageSet
from rendermodules.ingest.schemas import example as message_body_data

@pytest.fixture
def ref_set_ingest_message():
    example = message_body_data
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


@pytest.fixture
def em_montage_set_ingest_message():
    example = message_body_data
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
def test_reference_set_ingest(ref_set_ingest_message):
    mock_uuid = "MOCK_UUID"
    with patch('uuid.uuid4', Mock(return_value=mock_uuid)):
        LensCorrectionIngest().create_enqueued_object(
            ref_set_ingest_message,
            tags=["ReferenceSet"])

    ref_set = ReferenceSet.objects.get(uid=mock_uuid)
    assert ref_set is not None
    assert mock_uuid == ref_set.uid
    assert \
        ref_set_ingest_message['acquisition_data']['microscope'] == \
        ref_set.microscope.microscope_type.name
    assert \
        ref_set_ingest_message['acquisition_data']['camera']['camera_id'] == \
        ref_set.camera.uid
    assert \
        ref_set_ingest_message['acquisition_data']['camera']['height'] == \
        ref_set.camera.height
    assert \
        ref_set_ingest_message['acquisition_data']['camera']['width'] == \
        ref_set.camera.width
    assert ref_set_ingest_message['acquisition_data']['camera']['model'] == \
        ref_set.camera.model
    assert ref_set_ingest_message['metafile'] == ref_set.metafile
    assert ref_set_ingest_message['storage_directory'] == ref_set.storage_directory
    assert ref_set_ingest_message['manifest_path'] == ref_set.manifest_path
    # TODO: should reference set have an acquisition date
    # assert dateparse.parse_datetime(
    #     ref_set_ingest_message['acquisition_data']['acquisition_time']).astimezone(
    #         pytz.timezone('US/Pacific')) == \
    #     ref_set.acquisition_date


@pytest.mark.django_db
def test_em_montage_set_ingest(em_montage_set_ingest_message):
    em_montage_set_ingest_message['reference_set_id'] = "MOCK_REF_UUID"

    mock_uuid = "MOCK_UUID"
    with patch('uuid.uuid4', Mock(return_value=mock_uuid)):
        LensCorrectionIngest().create_enqueued_object(
            em_montage_set_ingest_message,
            tags=["EMMontageSet"])

    em_mset = EMMontageSet.objects.get(uid=mock_uuid)
    assert em_mset is not None
    assert mock_uuid == em_mset.uid
    assert \
        em_montage_set_ingest_message['acquisition_data']['microscope'] == \
        em_mset.microscope.microscope_type.name
    assert \
        em_montage_set_ingest_message[
            'acquisition_data']['camera']['camera_id'] == \
        em_mset.camera.uid
    assert \
        em_montage_set_ingest_message[
            'acquisition_data']['camera']['height'] == \
        em_mset.camera.height
    assert \
        em_montage_set_ingest_message[
            'acquisition_data']['camera']['width'] == \
        em_mset.camera.width
    assert \
        em_montage_set_ingest_message[
            'acquisition_data']['camera']['model'] == \
        em_mset.camera.model
    assert em_montage_set_ingest_message['metafile'] == em_mset.metafile
    assert \
        em_montage_set_ingest_message[
            'storage_directory'] == \
        em_mset.storage_directory
    # TODO: should reference set have an acquisition date
    # assert dateparse.parse_datetime(
    #     em_montage_set_ingest_message['acquisition_data']['acquisition_time']).astimezone(
    #         pytz.timezone('US/Pacific')) == \
    #     ref_set.acquisition_date
