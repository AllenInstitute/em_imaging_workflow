from mock import Mock, patch
import pytest
from django.test.utils import override_settings
from workflow_engine.models.job import Job
from workflow_engine.models.task import Task
from workflow_engine.workflow_controller import WorkflowController
from development.strategies.chmod_strategy import ChmodStrategy
from development.strategies.redirect_mip_maps_strategy \
    import RedirectMipMapsStrategy
from models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
import simplejson as json


@pytest.mark.django_db
def test_get_input_data(lots_of_montage_sets):
    em_mset = lots_of_montage_sets[0]
    task = Mock()
    task.job = Mock()
    storage_directory = '/example/storage/directory'
    strategy = RedirectMipMapsStrategy()
    
    with patch('os.makedirs'):
        with patch('os.path.exists', Mock(return_value=True)):
            inp = strategy.get_input(em_mset,
                                     storage_directory,
                                     task)

    assert inp['overwrite_zlayer'] == True
    assert set(inp['zValues']) == set([1])
    assert inp['input_stack'] == 'em_2d_montage_solved'
    assert inp['output_stack'] == 'em_2d_montage_redirect_mipmaps'
    assert inp['pool_size'] == 10
