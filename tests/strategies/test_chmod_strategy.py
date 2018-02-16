from mock import Mock, patch, call
import pytest
from development.strategies.chmod_strategy \
    import ChmodStrategy
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets


@pytest.mark.django_db
def test_get_input_data(lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]

    wkf = ChmodStrategy.add_chmod_dir(
        em_mset, '/path/to/chmod/dir')
    assert wkf.well_known_file_type == ChmodStrategy.CHMOD_DIR_PENDING
    wkf = ChmodStrategy.add_chmod_file(
        em_mset, '/path/to/chmod/dir')
    assert wkf.well_known_file_type == ChmodStrategy.CHMOD_FILE_PENDING
    wkf = ChmodStrategy.add_chmod_dir(
        em_mset, '/path/to/chmod/dir2')
    assert wkf.well_known_file_type == ChmodStrategy.CHMOD_DIR_PENDING

    task = Mock()
    storage_directory = '/example/storage/directory'
    strategy = ChmodStrategy()
    inp = strategy.get_input(em_mset,
                             storage_directory,
                             task)

    assert set(inp['dirs']) == set(['/path/to/chmod/dir/',
                                    '/path/to/chmod/dir2/'])
    assert set(inp['files']) == set(['/path/to/chmod/dir/'])

    processing = [
        ChmodStrategy.CHMOD_DIR_PROCESSING,
        ChmodStrategy.CHMOD_FILE_PROCESSING]

    wkfs = ChmodStrategy.find_chmod_files(
        em_mset,
        type_list=processing)

    assert len(wkfs) == 3

    for w in wkfs:
        assert w.well_known_file_type in processing
    
    results = { 'this': 'that'}
    strategy.on_finishing(em_mset, results, task)

    complete = [
        ChmodStrategy.CHMOD_DIR_COMPLETE,
        ChmodStrategy.CHMOD_FILE_COMPLETE]

    wkfs = ChmodStrategy.find_chmod_files(
        em_mset,
        type_list=complete)

    for w in wkfs:
        assert w.well_known_file_type in complete
