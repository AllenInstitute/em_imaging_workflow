import django
django.setup()
from django.test import TestCase
from django.utils import dateparse
import pytz
from development.management.commands.ingest_worker import Command 
from development.models.e_m_montage_set import EMMontageSet
from rendermodules.ingest.schemas import example as ex

class TestIngestWorker(TestCase):
    def test_example_input(self):
       example = ex
       Command.create_em_render_set(example)

       em_mset = EMMontageSet.objects.get(uid=example['reference_set_id'])
       assert em_mset is not None
       assert example['reference_set_id'] == em_mset.uid
       assert example['acquisition_data']['microscope'] == \
           em_mset.reference_set.microscope.microscope_type.name
       assert example['acquisition_data']['camera']['camera_id'] == \
           em_mset.reference_set.camera.uid
       assert example['acquisition_data']['camera']['height'] == \
           em_mset.reference_set.camera.height
       assert example['acquisition_data']['camera']['width'] == \
           em_mset.reference_set.camera.width
       assert example['acquisition_data']['camera']['model'] == \
           em_mset.reference_set.camera.model
       assert example['acquisition_data']['overlap'] == \
           em_mset.overlap
       assert dateparse.parse_datetime(
           example['acquisition_data']['acquisition_time']).astimezone(
               pytz.timezone('US/Pacific')) == \
           em_mset.acquisition_date
       assert example['section']['z_index'] == em_mset.section.z_index
       assert str(example['section']['specimen']) == \
           em_mset.section.specimen.uid
       assert example['section']['sample_holder'] == \
           em_mset.sample_holder.uid
       assert example['storage_directory'] == \
           em_mset.section.specimen.study.storage_directory 

