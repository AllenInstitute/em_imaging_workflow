import pytest
from django.conf import settings
from development.strategies.m_i_c_task_builder_strategy \
    import MICTaskBuilderStrategy
from mock import patch, mock_open, MagicMock

def test_get_input_data():
    em_mset = MagicMock()
    em_mset.section = MagicMock()
    test_z_index = 28990
    em_mset.section.z_index = test_z_index
    task = MagicMock()
    storage_directory = '/example/storage/directory'
    strategy = MICTaskBuilderStrategy()

    inp = strategy.get_input(em_mset,
                             storage_directory,
                             task)

    print(str(inp))
   
    assert inp is not None
    assert inp['render']['host'] == settings.RENDER_SERVICE_URL
    assert inp['render']['port'] == int(settings.RENDER_SERVICE_PORT)
    assert inp['render']['owner'] == settings.RENDER_SERVICE_USER
    assert inp['render']['project'] == settings.RENDER_SERVICE_PROJECT
    assert inp['render']['client_scripts'] == \
        settings.RENDER_CLIENT_SCRIPTS
    assert inp['input_stack'] == settings.RENDER_STACK_NAME
    assert inp['output_stack'] == settings.RENDER_STACK_NAME
    assert inp['minZ'] == test_z_index
    assert inp['maxZ'] == test_z_index
