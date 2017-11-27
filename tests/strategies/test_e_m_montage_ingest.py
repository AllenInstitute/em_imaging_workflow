import django
django.setup()
from django.test import TestCase
from django.utils import dateparse
import pytz
from unittest import skip
from development.strategies.lens_correction_ingest import LensCorrectionIngest
from development.strategies.e_m_montage_ingest import EMMontageIngest
from development.models.e_m_montage_set import EMMontageSet
from rendermodules.ingest.schemas import example as body_data


class TestEMMontageIngest(TestCase):
    @skip
    def test_example_input(self):
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

       reference_set = EMMontageIngest().create_enqueued_object(example)

       em_mset = EMMontageSet.objects.get(
           storage_directory=example['storage_directory'])
       assert em_mset is not None
       assert ref_body_data['reference_set_id'] == em_mset.reference_set.uid
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
       assert dateparse.parse_datetime(
           example['acquisition_data']['acquisition_time']).astimezone(
               pytz.timezone('US/Pacific')) == \
         em_mset.acquisition_date

