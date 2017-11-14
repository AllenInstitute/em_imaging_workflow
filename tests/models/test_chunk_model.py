import django
django.setup()
from django.test import TestCase
from development.models import Chunk, RenderedVolume, Study, Specimen
from django.test.utils import override_settings

class TestChunkModel(TestCase):
    def test_str(self):
        study = Study(
            name="Lorem Ipsum",
            storage_directory="/Lorem/ipsum/dolor/sit/amet/consectetur")
        specimen = Specimen(
            uid="DEADBEEF",
            render_project="ABCDEFG",
            render_owner="Whatever",
            study=study)
        rendered_volume = RenderedVolume(
            specimen=specimen,
            mipmap_directory="/Lorem/ipsum/dolor/sit/amet/consectetur")
        chuck = Chunk(size=20,
                      chunk_state="Something",
                      rendered_volume=rendered_volume)  # TODO: preceding and following
        self.assertEqual(str(chuck.rendered_volume.specimen.study), study.name)

    @override_settings(
        CHUNK_DEFAULTS={ 'overlap': 2, 'start_z': 1, 'chunk_size': 5 })
    def test_chunks_for_z_index(self):
       # TODO: 0?
       cks_1 = Chunk.chunks_for_z_index(1)
       cks_2 = Chunk.chunks_for_z_index(2)
       cks_3 = Chunk.chunks_for_z_index(3)
       cks_4 = Chunk.chunks_for_z_index(4)
       cks_5 = Chunk.chunks_for_z_index(5)
       cks_6 = Chunk.chunks_for_z_index(6)
       cks_7 = Chunk.chunks_for_z_index(7)
       cks_8 = Chunk.chunks_for_z_index(8)
       cks_9 = Chunk.chunks_for_z_index(9)
       cks_10 = Chunk.chunks_for_z_index(10)
       cks_11 = Chunk.chunks_for_z_index(11)
       cks_12 = Chunk.chunks_for_z_index(12)

       assert [0] == cks_1
       assert [0] == cks_2
       assert [0] == cks_3
       assert [0, 1] == cks_4
       assert [0, 1] == cks_5
       assert [1] == cks_6
       assert [1,2] == cks_7
       assert [1,2] == cks_8
       assert [2] == cks_9
       assert [2,3] == cks_10
       assert [2,3] == cks_11
       assert [3] == cks_12

    @override_settings(
        CHUNK_DEFAULTS={ 'overlap': 2, 'start_z': 1, 'chunk_size': 5 })
    def test_z_indices_for_chunk(self):
       # TODO: 0?
       cks_1 = Chunk.z_indices_for_chunk(0)
       assert [1,2,3,4,5] == cks_1
