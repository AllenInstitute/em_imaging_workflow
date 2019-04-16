import django
django.setup()
from django.test import TestCase
from at_em_imaging_workflow.models import Study, Specimen


class TestSpecimenModel(TestCase):
    def test_str(self):
        study = Study(
            name="Lorem Ipsum",
            storage_directory="/Lorem/ipsum/dolor/sit/amet/consectetur")
        specimen = Specimen(
            uid="DEADBEEF",
            render_project="ABCDEFG",
            render_owner="Whatever",
            study=study)
        self.assertEqual(str(specimen.study), study.name)
