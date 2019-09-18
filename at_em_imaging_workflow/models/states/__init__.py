''' Helpers to implement model states with the
`Django FSM <https://github.com/viewflow/django-fsm>`_ package.

Model states can be used for various purposes.

For example, they may indicate that an object is in or has passed (or not passed) 
a section of a workflow.
(for example Pending, Processing or Done).

They can also be used to distinguish objects at a coarse level
(for example PASSED, FAILED).

When used with a
:class:`workflow_engine.strategies.wait_strategy.WaitStrategy`
they can be used to indicate
when the object can proceed to the next workflow node
(for example MONTAGE_QC, CHUNK_INCOMPLETE)

'''
from .chunk_fsm import ChunkFsm
from .em_montage_set_state import EMMontageSetState
from .reference_set_state import ReferenceSetState
from .load_state import LoadState