import django
django.setup()
from django.test import TestCase
from development.models import RenderedVolumn, Study, Specimen


class TestRenderedVolumnModel(TestCase):
    def test_str(self):
        study = Study(
            name="Lorem Ipsum",
            storage_directory="/Lorem/ipsum/dolor/sit/amet/consectetur")
        specimen = Specimen(
            uid="DEADBEEF",
            render_project="ABCDEFG",
            render_owner="Whatever",
            study=study)
        rendered_volumn = RenderedVolumn(
            specimen=specimen,
            mipmap_directory="/Lorem/ipsum/dolor/sit/amet/consectetur")
        self.assertEqual(str(rendered_volumn.specimen.study), study.name)
