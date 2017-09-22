from django.test import TestCase
from development.models import Study


class TestStudyModel(TestCase):
    def test_str(self):
        study = Study(
            name="Lorem Ipsum",
            storage_directory="/Lorem/ipsum/dolor/sit/amet/consectetur")
        self.assertEqual(str(study), study.name)
