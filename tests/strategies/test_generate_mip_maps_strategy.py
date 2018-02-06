import pytest
from django.test.utils import override_settings
from mock import Mock, patch
from tests.models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from development.strategies.generate_mip_maps_strategy \
    import GenerateMipMapsStrategy

@pytest.mark.django_db
@override_settings(
    RENDER_SERVICE_URL='MOCK_URL',
    RENDER_SERVICE_PORT=9999,
    RENDER_SERVICE_USER='MOCK_USER',
    RENDER_CLIENT_SCRIPTS='/path/to/mock/client/scripts',
    MIPMAP_FILE_PATH='/path/to/mipmaps',
)
def test_get_input_data(lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    task = Mock()
    task.job = Mock()
    storage_directory = '/example/storage/directory'
    strategy = GenerateMipMapsStrategy()
    
    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            inp = strategy.get_input(em_mset,
                                       storage_directory,
                                       task)
    assert inp['output_dir'].startswith('/path/to/mipmaps')

