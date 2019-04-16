# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2017. Allen Institute. All rights reserved.
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
from mock import patch, mock_open
import django.test
from django.conf import settings
from workflow_engine.workflow_config import WorkflowConfig
from tests.workflow_configurations import TEST_CONFIG_YAML_TWO_NODES
import simplejson as json
import os
from at_em_imaging_workflow.models.chunk import Chunk
from at_em_imaging_workflow.strategies.rough.define_chunks_strategy import DefineChunksStrategy
from django.test.utils import override_settings
from at_em_imaging_workflow.views.page_satchel import page_satchel
from workflow_engine.models.job import Job
from workflow_engine.models.workflow_node import WorkflowNode
from workflow_engine.models.run_state import RunState
from workflow_engine.workflow_controller import WorkflowController
from tests.models.test_chunk_model \
    import cameras_etc, section_factory, lots_of_montage_sets
from django.utils.six import BytesIO


@pytest.fixture
def rf():
    return django.test.RequestFactory()


@pytest.mark.django_db
@override_settings(
    CHUNK_DEFAULTS = {
        'overlap': 100,
        'start_z': 1,
        'chunk_size': 200 })
def test_temca_query(rf,
                    lots_of_montage_sets):
    for em_mset in lots_of_montage_sets:
        strat = DefineChunksStrategy()
        strat.must_wait(em_mset)

    #assert Chunk.objects.count() == 125

    request = rf.get(
        '/at_em/page_satchel?q=temca_query&scope=MOCK MICROSCOPE')
    response = page_satchel(request)
    assert response.status_code == 200

    result_data = json.load(BytesIO(response.content))
    assert result_data['success'][0] == True
    assert len(result_data['message']['MOCK MICROSCOPE']) == 999
    #assert json.dumps(result_data, indent=2) == '' 

@pytest.mark.django_db
@pytest.mark.skipif(True, reason='deprecated')
def test_find_sections(rf,
                    lots_of_montage_sets):
    yaml_text = TEST_CONFIG_YAML_TWO_NODES

    with patch("builtins.open",
        mock_open(read_data=yaml_text)):
        WorkflowConfig.create_workflow(
            os.path.join(os.path.dirname(__file__),
                         'dev.yml'))

        for em_mset in lots_of_montage_sets:
            WorkflowController.enqueue_object(
                WorkflowNode.objects.first(),
                em_mset)

        request = rf.get(
            '/at_em/page_satchel?q=find_sections'
            '&workflow=test_workflow'
            '&zs=2,4,20')
        response = page_satchel(request)
        assert response.status_code == 200

    result_data = json.load(BytesIO(response.content))

    assert result_data['success'] == True
    assert len(result_data['message'].keys()) == 3
    assert set(r['z']
        for r in result_data['message'].values()) == { 2, 4, 20}
    assert set(r['montage set id']
        for r in result_data['message'].values()) == {31982, 31984, 32000}
    for r in result_data['message'].values():
        assert r['run state'] == 'PENDING'
        assert r['job queue'] == 'Start'
    # assert json.dumps(result_data, indent=2) == '' 
