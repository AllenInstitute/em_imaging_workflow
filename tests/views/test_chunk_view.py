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
from at_em_imaging_workflow.views import chunk_view
from workflow_engine.workflow_config import WorkflowConfig
import simplejson as json
import os
from lxml import etree
from development.models.chunk import Chunk
from development.strategies.define_chunks_strategy import DefineChunksStrategy
from django.test.utils import override_settings
from models.test_chunk_model \
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
def test_chunk_view(rf,
                    lots_of_montage_sets):
    for em_mset in lots_of_montage_sets:
        strat = DefineChunksStrategy()
        strat.must_wait(em_mset)

    #assert Chunk.objects.count() == 125

    request = rf.get('/at_em_imaging_workflow/chunks.html')
    response = chunk_view.chunks_page(request)
    assert response.status_code == 200

    html_parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(response.content),
                       html_parser)

    tbl = tree.xpath('//table[@id="chnk_table"]')
    #assert len(tbl) == 1
    #assert tbl[0].tag == 'table'
    trs = tbl[0].xpath('tr[@class="chnk_tr"]')
    #assert len(trs) == 125

    for tr in trs:
        tds = tr.xpath('td')
        #assert len(tds) == settings.CHUNK_DEFAULTS['chunk_size'] + 1

    with open('test_view.html', 'w') as f:
        f.write(
            etree.tostring(tree,
                pretty_print=True,
               method='html').decode('utf-8'))
