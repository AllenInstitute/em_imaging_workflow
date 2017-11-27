import django
django.setup()
from django.test import TestCase
from django.utils import dateparse
import os
import pytz
from development.strategies.lens_correction_ingest import LensCorrectionIngest
from development.models.reference_set import ReferenceSet
from rendermodules.ingest.schemas import example as message_body_data

class TestIngestReferenceSet(TestCase):
    def test_example_input(self):
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
       LensCorrectionIngest().create_enqueued_object(example)

       ref_set = ReferenceSet.objects.get(uid=example['reference_set_id'])
       assert ref_set is not None
       assert example['reference_set_id'] == ref_set.uid
       assert example['acquisition_data']['microscope'] == \
           ref_set.microscope.microscope_type.name
       assert example['acquisition_data']['camera']['camera_id'] == \
           ref_set.camera.uid
       assert example['acquisition_data']['camera']['height'] == \
           ref_set.camera.height
       assert example['acquisition_data']['camera']['width'] == \
           ref_set.camera.width
       assert example['acquisition_data']['camera']['model'] == \
           ref_set.camera.model
       assert example['metafile'] == ref_set.metafile
       assert example['storage_directory'] == ref_set.storage_directory
       assert example['manifest_path'] == ref_set.manifest_path
       # TODO: should reference set have an acquisition date
       # assert dateparse.parse_datetime(
       #     example['acquisition_data']['acquisition_time']).astimezone(
       #         pytz.timezone('US/Pacific')) == \
       #     ref_set.acquisition_date

