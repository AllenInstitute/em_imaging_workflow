import django
django.setup()
from django.test import TestCase
from django.utils import dateparse
import pytz
from development.management.commands.ingest_worker import Command 
from development.management.commands.ingest_reference_set import Command as Ref
from development.models.e_m_montage_set import EMMontageSet
from rendermodules.ingest.schemas import example as body_data
from pikatest_reference import message_body_data as ref_body_data

class TestIngestWorker(TestCase):
    def test_example_input(self):
       ref_set = Ref.create_reference_set(ref_body_data)

       example = body_data
       example['reference_set_id'] = ref_body_data['reference_set_id']
       reference_set = Command.create_em_render_set(example)

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

