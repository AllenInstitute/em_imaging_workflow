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
from at_em_imaging_workflow.two_d_stack_name_manager \
    import TwoDStackNameManager
from mock import Mock


@pytest.fixture
def ref_set():
    ref_set = Mock()
    ref_set.reimage_index = Mock(return_value=0)

    return ref_set

@pytest.fixture
def em_mset():
    em_mset = Mock()
    em_mset.reimage_index = Mock(return_value=0)

    return em_mset


@pytest.fixture
def em_mset_reimage_one():
    em_mset = Mock()
    em_mset.reimage_index = Mock(return_value=1)

    return em_mset


def test_mesh_lens_correction_stacks(ref_set):
    stacks = TwoDStackNameManager.mesh_lens_correction_stacks(ref_set)

    assert stacks['input_stack'] == 'em_2d_raw_lc_stack'
    assert stacks['output_stack'] == 'em_2d_lc_corrected'


def test_generate_render_stack_stacks(em_mset):
    stacks = TwoDStackNameManager.generate_render_stack_stacks(em_mset)

    assert stacks['output_stack'] == 'em_2d_montage_ingest'


def test_generate_render_stack_stacks_reimage(em_mset_reimage_one):
    stacks = TwoDStackNameManager.generate_render_stack_stacks(
        em_mset_reimage_one)

    assert stacks['output_stack'] == 'em_2d_montage_ingest_reimage_1'

def test_generate_mip_maps_stacks(em_mset):
    stacks = TwoDStackNameManager.generate_mip_maps_stacks(em_mset)

    assert stacks['input_stack'] == 'em_2d_montage_ingest'


def test_apply_mip_maps_stacks(em_mset):
    stacks = TwoDStackNameManager.apply_mip_maps_stacks(em_mset)

    assert stacks['input_stack'] == 'em_2d_montage_ingest'
    assert stacks['output_stack'] == 'em_2d_montage_apply_mipmaps'


def test_apply_lens_correction_stacks(em_mset):
    stacks = TwoDStackNameManager.apply_lens_correction_stacks(em_mset)

    assert stacks['input_stack'] == 'em_2d_montage_apply_mipmaps'
    assert stacks['output_stack'] == 'em_2d_montage_lc'


def test_apply_lens_correction_stacks_reimage(em_mset_reimage_one):
    stacks = TwoDStackNameManager.apply_lens_correction_stacks(
        em_mset_reimage_one)

    assert stacks['input_stack'] == 'em_2d_montage_apply_mipmaps_reimage_1'
    assert stacks['output_stack'] == 'em_2d_montage_lc_reimage_1'


def test_create_tile_pairs_stacks(em_mset):
    stacks = TwoDStackNameManager.create_tile_pairs_stacks(em_mset)

    assert stacks['baseStack'] == 'em_2d_montage_lc'
    assert stacks['stack'] == 'em_2d_montage_lc'


def test_create_tile_pairs_stacks_reimage(em_mset_reimage_one):
    stacks = TwoDStackNameManager.create_tile_pairs_stacks(em_mset_reimage_one)

    assert stacks['baseStack'] == 'em_2d_montage_lc_reimage_1'
    assert stacks['stack'] == 'em_2d_montage_lc_reimage_1'


def test_two_d_solver_stacks(em_mset):
    stacks = TwoDStackNameManager.two_d_solver_stacks(em_mset)

    assert stacks['source_collection'] == 'em_2d_montage_lc'
    assert stacks['target_collection'] == 'em_2d_montage_solved'


def test_two_d_solver_stacks_reimage(em_mset_reimage_one):
    stacks = TwoDStackNameManager.two_d_solver_stacks(em_mset_reimage_one)

    assert stacks['source_collection'] == 'em_2d_montage_lc_reimage_1'
    assert stacks['target_collection'] == 'em_2d_montage_solved_reimage_1'


def test_two_d_solver_python_stacks(em_mset):
    stacks = TwoDStackNameManager.two_d_python_solver_stacks(em_mset)

    assert stacks['input_stack'] == 'em_2d_montage_lc'
    assert stacks['output_stack'] == 'em_2d_montage_solved_py'


def test_two_d_solver_python_stacks_reimage(em_mset_reimage_one):
    stacks = TwoDStackNameManager.two_d_python_solver_stacks(
        em_mset_reimage_one)

    assert stacks['input_stack'] == 'em_2d_montage_lc_reimage_1'
    assert stacks['output_stack'] == 'em_2d_montage_solved_py_reimage_1'


def test_detect_defects_stacks(em_mset):
    stacks = TwoDStackNameManager.detect_defects_stacks(em_mset)

    assert stacks['prestitched_stack'] == 'em_2d_montage_lc'
    assert stacks['poststitched_stack'] == 'em_2d_montage_solved_py'


def test_detect_defects_stacks_reimage(em_mset_reimage_one):
    stacks = TwoDStackNameManager.detect_defects_stacks(
        em_mset_reimage_one)

    assert stacks['prestitched_stack'] == 'em_2d_montage_lc_reimage_1'
    assert stacks['poststitched_stack'] == 'em_2d_montage_solved_py_reimage_1'


def test_make_montage_scapes_stacks(em_mset):
    stacks = TwoDStackNameManager.make_montage_scapes_stacks(em_mset)

    assert stacks['montage_stack'] == 'em_2d_montage_solved_py'
    assert stacks['output_stack'] == 'em_2d_montage_solved_py_0_01_mapped'


def test_make_montage_scapes_stacks_reimage(em_mset_reimage_one):
    stacks = TwoDStackNameManager.make_montage_scapes_stacks(
        em_mset_reimage_one)

    assert stacks['montage_stack'] == 'em_2d_montage_solved_py_reimage_1'
    assert stacks['output_stack'] == \
        'em_2d_montage_solved_py_0_01_mapped_reimage_1'


def test_remap_z_stacks(em_mset):
    stacks = TwoDStackNameManager.remap_z_stacks(em_mset)

    assert stacks['input_stack'] == 'em_2d_montage_solved_py_0_01_mapped'
    assert stacks['output_stack'] == 'em_2d_montage_downsampled_no_mapping'


def test_remap_z_stacks_reimage(em_mset_reimage_one):
    stacks = TwoDStackNameManager.remap_z_stacks(
        em_mset_reimage_one)

    assert stacks['input_stack'] == \
        'em_2d_montage_solved_py_0_01_mapped_reimage_1'
    assert stacks['output_stack'] == \
        'em_2d_montage_downsampled_no_mapping_reimage_1'

