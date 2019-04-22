# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2019. Allen Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Redistributions for commercial purposes are not permitted without the
# Allen Institute's written permission.
# For purposes of this license, commercial purposes is the incorporation of the
# Allen Institute's software into anything for which you will charge fees or
# other compensation. Contact terms@alleninstitute.org for commercial licensing
# opportunities.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
import pytest
from mock import patch, MagicMock, Mock
from at_em_imaging_workflow.strategies.fusion.register_adjacent_stack_strategy \
    import RegisterAdjacentStackStrategy
from tests.fixtures.model_fixtures import (
    cameras_etc,
    section_factory,
    lots_of_montage_sets,
    lots_of_chunks
)
import simplejson as json


@pytest.mark.django_db
@patch(
    'at_em_imaging_workflow.strategies.fusion.'
    'register_adjacent_stack_strategy.RegisterAdjacentStackStrategy.'
    'get_workflow_node_input_template',
    Mock(return_value={
    })
)
def test_get_input_data(lots_of_chunks):
    chnk = lots_of_chunks[4]
    task = MagicMock()
    storage_directory = '/example/storage/directory'
    strategy = RegisterAdjacentStackStrategy()

    input_ret = strategy.get_input(chnk,
                                   storage_directory,
                                   task)

    assert input_ret is not None
    #raise Exception(json.dumps(input_ret, indent=2))


