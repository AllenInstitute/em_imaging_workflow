import pytest
from development.strategies.downsample_section_image_strategy \
    import DownsampleSectionImageStrategy

def test_get_input_data():
    enqueued_object = None
    task = None
    storage_directory = '/example/storage/directory'
    strategy = DownsampleSectionImageStrategy()
    input = strategy.get_input(enqueued_object,
                               storage_directory,
                               task)
    assert input is not None
