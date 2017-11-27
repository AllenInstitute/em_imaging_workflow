import django
django.setup()
from django.test import TestCase
from django.utils import dateparse
import os
import pytz
from development.management.commands.ingest_reference_set import Command 
from development.models.reference_set import ReferenceSet
from pikatest_reference import message_body_data

class TestIngestReferenceSet(TestCase):
    def test_example_input(self):
       example = message_body_data
       Command.create_reference_set(example)

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
       assert os.path.dirname(example['acquisition_data']['metafile']) == \
           ref_set.storage_directory
       # TODO: should reference set have an acquisition date
       # assert dateparse.parse_datetime(
       #     example['acquisition_data']['acquisition_time']).astimezone(
       #         pytz.timezone('US/Pacific')) == \
       #     ref_set.acquisition_date

