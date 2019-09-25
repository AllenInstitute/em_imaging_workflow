import pytest
from django.test.utils import override_settings
from workflow_engine.models import Job
from at_em_imaging_workflow.models import (
    ChunkAssignment,
    EMMontageSet
)
from at_em_imaging_workflow.strategies.rough.define_chunks_strategy import (
    DefineChunksStrategy
)
from tests.fixtures.model_fixtures import (
    cameras_etc,           # noqa # pylint: disable=unused-import
    section_factory,       # noqa # pylint: disable=unused-import
    lots_of_montage_sets,  # noqa # pylint: disable=unused-import
    lots_of_chunks         # noqa # pylint: disable=unused-import
)


@pytest.mark.unimplemented
@pytest.mark.django_db
@override_settings(
    BASE_FILE_PATH='/base',
    LONG_TERM_BASE_FILE_PATH='/long/term',
    RENDER_STACK_NAME='test_stack',
    RENDER_SERVICE_USER='test_user',
    RENDER_SERVICE_URL='test_render_host',
    RENDER_SERVICE_PORT='1234',
    RENDER_CLIENT_SCRIPTS='/path/to/test/client/scripts'
    )
def test_must_wait(lots_of_chunks):
    strat = DefineChunksStrategy()
    chnk = lots_of_chunks[0]
    computed_index = chnk.computed_index

    montage_sets = [
        s.montageset_set.get().emmontageset
        for s in chnk.sections.all()
    ]
    ChunkAssignment.objects.filter(chunk=chnk).delete()
    n = len(montage_sets)

    for i in range(0, n):
        em_mset = montage_sets[i]
        em_mset.object_state = EMMontageSet.STATE.EM_MONTAGE_SET_QC_PASSED
        em_mset.save()

        j = Job(enqueued_object=em_mset)
        cs = strat.get_objects_for_queue(j)

        cs = [c for c in cs if c.computed_index == computed_index]
        assert len(cs) == 1

        c = cs[0]
        waiting = strat.must_wait(c)

        if i == n - 1:
            assert c.is_complete()
            assert len(c.missing_sections()) == 0
            assert not waiting
        else:
            assert not c.is_complete()
            assert len(c.missing_sections()) > 0
            assert waiting
