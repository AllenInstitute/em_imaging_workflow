#import django
#django.setup()
from django.test import TestCase
from development.models import ReferenceSet


class TestReferenceSet(TestCase):
    def test_str(self):
        ref_set = ReferenceSet(
            project_path="/path/to/project/lorem/ipsum")
        self.assertEqual("/path/to/project/lorem/ipsum",
                         ref_set.project_path)
