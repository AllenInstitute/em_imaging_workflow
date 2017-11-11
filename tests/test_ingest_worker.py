import django
django.setup()
from django.test import TestCase
from django.utils import dateparse
import pytz
from development.management.commands.ingest_worker import Command 
from development.management.commands.ingest_reference_set import Command as Ref
from development.models.e_m_montage_set import EMMontageSet
from rendermodules.ingest.schemas import example as ex
from pikatest_reference import ex as ex_ref

class TestIngestWorker(TestCase):
    def test_example_input(self):
       ref_set = Ref.create_reference_set(ex_ref)

       example = ex
       Command.create_em_render_set(example)

       em_mset = EMMontageSet.objects.get(
           storage_directory=example['storage_directory'])
       assert em_mset is not None
       assert example['reference_set_id'] == em_mset.reference_set.uid
       assert example['acquisition_data']['overlap'] == em_mset.overlap
       assert example['storage_directory'] == em_mset.storage_directory
       assert example['section']['z_index'] == em_mset.section.z_index
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

