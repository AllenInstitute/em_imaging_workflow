import django
django.setup()
from django.test import TestCase
from development.strategies.lens_correction_ingest import LensCorrectionIngest
from development.strategies.e_m_montage_ingest import EMMontageIngest
from development.models.e_m_montage_set import EMMontageSet
from rendermodules.ingest.schemas import example as body_data
import copy

class TestEMMontageIngest(TestCase):
    def test_with_reference_set(self):
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

       ref_set = LensCorrectionIngest().create_enqueued_object(example)
       em_mset = EMMontageIngest().create_enqueued_object(example)

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

    def test_without_reference_set(self):
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

       em_mset = EMMontageIngest().create_enqueued_object(example)

       assert em_mset is not None

       get_em_mset = EMMontageSet.objects.get(
           storage_directory=example['storage_directory'])

       assert get_em_mset is not None
       assert em_mset.reference_set is None
       assert em_mset.reference_set_uid is None
       assert body_data['acquisition_data']['overlap'] == em_mset.overlap
       assert example['storage_directory'] == em_mset.storage_directory
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

