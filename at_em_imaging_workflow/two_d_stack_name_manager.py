# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2018. Allen Institute. All rights reserved.
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
import os

class TwoDStackNameManager(object):
    RENDER_STACK_INGEST = 'em_2d_montage_ingest{}'
    RENDER_STACK_LENS_CORRECTED = 'em_2d_montage_lc{}'
    RENDER_STACK_MESH_LENS_RAW = 'em_2d_raw_lc_stack'
    RENDER_STACK_MESH_LENS_CORRECTED = 'em_2d_lc_corrected'
    RENDER_LENS_COLLECTION = 'em_2d_lens_matches'
    RENDER_STACK_APPLY_MIPMAPS = 'em_2d_montage_apply_mipmaps{}'
    RENDER_STACK_TILE_PAIRS = 'em_2d_montage_tile_pairs'
    RENDER_STACK_POINT_MATCH = 'em_2d_montage_point_match'
    RENDER_STACK_SOLVED = 'em_2d_montage_solved{}'
    RENDER_STACK_SOLVED_PYTHON = 'em_2d_montage_solved_py{}'
    RENDER_STACK_REDIRECT_MIPMAPS = 'em_2d_montage_redirect_mipmaps'
    #RENDER_STACK_DOWNSAMPLED = 'em_2d_montage_downsampled_no_scale_z_mapped'
    RENDER_STACK_DOWNSAMPLED = 'em_2d_montage_solved_py_0_01_mapped{}'
    # RENDER_STACK_DOWNSAMPLED_UNMAPPED = 'em_2d_montage_downsampled_no_scale_no_mapping'
    RENDER_STACK_DOWNSAMPLED_UNMAPPED = 'em_2d_montage_downsampled_no_mapping{}'

    RENDER_STACK_RIGID_ALIGN_DOWNSAMPLE = \
        'em_rigid_align_solved_downsample_zs{}_ze{}'
    RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE = \
        'em_rough_align_solved_downsample_zs{}_ze{}'
    RENDER_STACK_MONTAGE_SCAPES_STACK = \
        'em_montage_scapes_zs_{}_ze_{}'
    RENDER_STACK_ROUGH_ALIGN = 'em_rough_align_zs{}_ze{}'
    RENDER_STACK_ROUGH_SOLVED = 'em_rough_align_zs{}_ze{}_solved'

    RENDER_STACK_FUSION = 'FUSEDOUTSTACK'

    POINT_MATCH_FILTER_JSON = 'point_match_filter{}_z_{}_to_{}.json'

    ROUGH_POINT_MATCH_COLLECTION = 'chunk_rough_align_point_matches'


    class TRANSFORM:
        RIGID = 'rigid'
        AFFINE = 'affine'

    @classmethod
    def mesh_lens_correction_raw_stack(cls, ref_set):
        return cls.RENDER_STACK_MESH_LENS_RAW

    @classmethod
    def mesh_lens_corrected_stack(cls, ref_set):
        return cls.RENDER_STACK_MESH_LENS_CORRECTED

    @classmethod
    def mesh_lens_correction_stacks(cls, ref_set):
        return {
            'input_stack': cls.mesh_lens_correction_raw_stack(ref_set),
            'output_stack': cls.mesh_lens_corrected_stack(ref_set)
        }

    @classmethod
    def raw_stack(cls, em_mset):
        return cls.RENDER_STACK_INGEST.format(
            cls.get_reimage_suffix(em_mset))

    @classmethod
    def applied_mip_maps_stack(cls, em_mset):
        return cls.RENDER_STACK_APPLY_MIPMAPS.format(
            cls.get_reimage_suffix(em_mset))

    @classmethod
    def get_reimage_suffix(cls, em_mset):
        if em_mset is None:
            reimage_suffix = ''
        else:
            reimage_level = em_mset.reimage_index()

            if reimage_level:
                reimage_suffix = '_reimage_{}'.format(reimage_level)
            else:
                reimage_suffix = ''

        return reimage_suffix

    @classmethod
    def lens_corrected_stack(cls, em_mset):
        return cls.RENDER_STACK_LENS_CORRECTED.format(
            cls.get_reimage_suffix(em_mset))

    @classmethod
    def point_match_collection(cls, em_mset):
        return em_mset.get_point_collection_name()

    @classmethod
    def rough_point_match_collection(cls, chnk):
        return cls.ROUGH_POINT_MATCH_COLLECTION

    @classmethod
    def point_match_filter_json(cls, em_mset):
        return os.path.join(
            em_mset.get_storage_directory(),
            cls.POINT_MATCH_FILTER_JSON.format(
                cls.get_reimage_suffix(em_mset),
                em_mset.section.z_index,
                em_mset.section.z_index
            )
        )

    @classmethod
    def solved_stack(cls, em_mset):
        return cls.RENDER_STACK_SOLVED.format(
            cls.get_reimage_suffix(em_mset))


    @classmethod
    def solved_python_stack(cls, em_mset):
        return cls.RENDER_STACK_SOLVED_PYTHON.format(
            cls.get_reimage_suffix(em_mset))


    @classmethod
    def downsampled_stack(cls, em_mset):
        if em_mset:
            suffix = cls.get_reimage_suffix(em_mset)
        else:
            suffix = ''

        return cls.RENDER_STACK_DOWNSAMPLED.format(
            suffix)


    @classmethod
    def downsampled_unmapped_stack(cls, em_mset):
        if em_mset:
            suffix = cls.get_reimage_suffix(em_mset)
        else:
            suffix = ''

        return cls.RENDER_STACK_DOWNSAMPLED_UNMAPPED.format(
            suffix)

    @classmethod
    def render_adjacent_stack_a(cls, chnk):
        return cls.RENDER_STACK_FUSION_A

    @classmethod
    def render_adjacent_stack_b(cls, chnk):
        return cls.RENDER_STACK_FUSION_B

    @classmethod
    def generate_render_stack_stacks(cls, em_mset):
        return {
            'output_stack': cls.raw_stack(em_mset)
        }

    @classmethod
    def generate_mip_maps_stacks(cls, em_mset):
        return {
            'input_stack': cls.raw_stack(em_mset)
        }

    @classmethod
    def apply_mip_maps_stacks(cls, em_mset):
        return {
            'input_stack': cls.raw_stack(em_mset),
            'output_stack': cls.applied_mip_maps_stack(em_mset)
        }

    @classmethod
    def apply_lens_correction_stacks(cls, em_mset):
        return {
            'input_stack': cls.applied_mip_maps_stack(em_mset),
            'output_stack': cls.lens_corrected_stack(em_mset)
        }

    @classmethod
    def create_tile_pairs_stacks(cls, em_mset):
        return {
            'baseStack': cls.lens_corrected_stack(em_mset),
            'stack': cls.lens_corrected_stack(em_mset)
        }

    @classmethod
    def two_d_solver_stacks(cls, em_mset):
        return {
            'source_collection': cls.lens_corrected_stack(em_mset),
            'target_collection': cls.solved_stack(em_mset)
        }

    @classmethod
    def two_d_python_solver_stacks(cls, em_mset):
        return {
            'input_stack': cls.lens_corrected_stack(em_mset),
            'output_stack': cls.solved_python_stack(em_mset)
        }

    @classmethod
    def detect_defects_stacks(cls, em_mset):
        return {
            'prestitched_stack': cls.lens_corrected_stack(em_mset),
            'poststitched_stack': cls.solved_python_stack(em_mset)
        }

    @classmethod
    def make_montage_scapes_stacks(cls, em_mset):
        return {
            'montage_stack': cls.solved_python_stack(em_mset),
            'output_stack': cls.downsampled_stack(em_mset)
        }

    @classmethod
    def remap_z_stacks(cls, em_mset):
        return {
            'input_stack': cls.downsampled_stack(em_mset),
            'output_stack': cls.downsampled_unmapped_stack(em_mset)
        }

    @classmethod
    def create_rough_pair_stacks(cls, chk_assn):
        return {
            'baseStack': cls.downsampled_stack(None),
            'stack': cls.downsampled_stack(None)
        }

    @classmethod
    def rigid_align_downsample_stack(cls, chnk):
        zs = chnk.get_z_mapping().values()
        min_z = min(zs)
        max_z = max(zs)

        return cls.RENDER_STACK_RIGID_ALIGN_DOWNSAMPLE.format(min_z, max_z)

    @classmethod
    def rough_align_downsample_stack(cls, chnk):
        zs = chnk.get_z_mapping().values()
        min_z = min(zs)
        max_z = max(zs)

        return cls.RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE.format(min_z, max_z)

    @classmethod
    def rough_align_stack(cls, chnk):
        zs = chnk.get_z_mapping().values()
        min_z = min(zs)
        max_z = max(zs)

        return cls.RENDER_STACK_ROUGH_ALIGN.format(min_z, max_z)

    @classmethod
    def solve_rough_align_stacks(cls, chnk):
        return {
            'source': cls.downsampled_stack(None),
            'target': cls.rough_align_downsample_stack(chnk)
        }

    @classmethod
    def solve_rough_align_python_stacks(cls, chnk, transformation):
        if transformation == TwoDStackNameManager.TRANSFORM.RIGID:
            return {
                'input_stack': cls.downsampled_stack(None),
                'output_stack': cls.rigid_align_downsample_stack(chnk)
            }
        elif transformation == TwoDStackNameManager.TRANSFORM.AFFINE:
            return {
                'input_stack': cls.rigid_align_downsample_stack(chnk),
                'output_stack': cls.rough_align_downsample_stack(chnk)
            }
        else:
            raise Exception(
                'transformation must be {} or {}'.format(
                    TwoDStackNameManager.TRANSFORM.RIGID,
                    TwoDStackNameManager.TRANSFORM.AFFINE
                ))

    @classmethod
    def apply_rough_alignment_stacks(cls, chnk):
        return {
            'montage_stack': cls.solved_python_stack(None),
            'prealigned_stack': cls.solved_python_stack(None),
            'lowres_stack': cls.rough_align_downsample_stack(chnk),
            'output_stack': cls.rough_align_stack(chnk)
        }

    @classmethod
    def register_adjacent_stacks(cls, chnk):
        return {
            'stack_a': cls.rough_align_stack(
                chnk.preceding_chunk
            ),
            'stack_b': cls.rough_align_stack(
                chnk
            )
        }

    # stack is same input stack as point match
    # input/output point match collection is default
    # full path to filter output file, similar to tile pair json
    # output file is also in output json, drop it on an mset config
    @classmethod
    def filter_point_match_stacks(cls, em_mset):
        stacks = {
            'input_stack': cls.lens_corrected_stack(em_mset),
            'input_match_collection': cls.point_match_collection(em_mset),
            'output_match_collection': cls.point_match_collection(em_mset),
            'output_json': cls.point_match_filter_json(em_mset),
            'filter_output_file': cls.point_match_filter_json(em_mset)
        }

        return stacks

    @classmethod
    def swap_zs_stacks(cls, em_mset, reimaged_mset):
        stacks = {
            'source_stack': [
                cls.raw_stack(em_mset),
                cls.lens_corrected_stack(em_mset),
                cls.applied_mip_maps_stack(em_mset),
                cls.solved_python_stack(em_mset),
                cls.downsampled_stack(em_mset),
                cls.downsampled_unmapped_stack(em_mset)
            ],
            'target_stack': [
                cls.raw_stack(reimaged_mset),
                cls.lens_corrected_stack(reimaged_mset),
                cls.applied_mip_maps_stack(reimaged_mset),
                cls.solved_python_stack(reimaged_mset),
                cls.downsampled_stack(reimaged_mset),
                cls.downsampled_unmapped_stack(reimaged_mset)
            ]
        }

        return stacks

    @classmethod
    def swap_point_match_collections(cls, em_mset, reimaged_mset):
        stacks = {
            'source_collection': cls.point_match_collection(em_mset),
            'target_collection': cls.point_match_collection(reimaged_mset)
        }

        return stacks
