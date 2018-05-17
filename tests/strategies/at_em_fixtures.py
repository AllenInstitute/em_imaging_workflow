import pytest


@pytest.fixture
def mock_run_states():
    rs = {}
    for s in [
        'PENDING',
        'QUEUED',
        'RUNNING',
        'FINISHED_EXECUTION',
        'FAILED_EXECUTION',
        'SUCCESS',
        'FAILED']:
        rs[s], _ = RunState.objects.update_or_create(
            name=s)
    return rs


from workflow_engine.models.run_state import RunState
