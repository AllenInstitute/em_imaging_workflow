import pytest
from tests.fixtures.model_fixtures import (
    cameras_etc,
    section_factory, 
    mock_tile_set
)


@pytest.mark.django_db
def test_get_section_index_queries(mock_tile_set):
    assert mock_tile_set.get_section_z_index() == 10001
