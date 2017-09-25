import django
django.setup()
from django.test import TestCase
from development.models import Chuck, RenderedVolumn, Study, Specimen


class TestChuckModel(TestCase):
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
        chuck = Chuck(size=20,
                      chunk_state="Something",
                      rendered_volumn=rendered_volumn)  # TODO: prececing and following
        self.assertEqual(str(chuck.rendered_volumn.specimen.study), study.name)
