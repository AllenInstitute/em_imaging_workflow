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
from mock import patch, mock_open, MagicMock, Mock
from at_em_imaging_workflow.strategies.montage.apply_lens_correction_strategy \
    import ApplyLensCorrectionStrategy


@pytest.mark.django_db
@patch(
    'at_em_imaging_workflow.strategies.montage.'
    'apply_lens_correction_strategy.ApplyLensCorrectionStrategy.'
    'get_workflow_node_input_template',
    Mock(return_value={
        'overwrite_zlayer': True
    })
)
def test_get_input_data():
    em_mset = MagicMock()
    em_mset.section = MagicMock()
    test_z_index = 543
    em_mset.section.z_index = test_z_index
    em_mset.metafile = '/path/to/test/meta.file'
    em_mset.reimage_index = MagicMock(return_value=0)
    task = MagicMock()
    wkf_mock = MagicMock()
    wkf_mock.get = MagicMock(return_value='/path/to/xform.json')
    storage_directory = '/example/storage/directory'
    strategy = ApplyLensCorrectionStrategy()
    with patch('workflow_engine.models.well_known_file.WellKnownFile',
               wkf_mock):
        with patch("builtins.open",
                   mock_open(read_data='{ "transform": "TEST_XFM" }')):
            input_ret = strategy.get_input(em_mset,
                                           storage_directory,
                                           task)

    assert input_ret['overwrite_zlayer'] == True
    assert set(input_ret['zValues']) == set([543])
    assert input_ret['input_stack'] == 'em_2d_montage_apply_mipmaps'
    assert input_ret['output_stack'] == 'em_2d_montage_lc'
