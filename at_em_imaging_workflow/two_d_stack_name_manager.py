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
    RENDER_STACK_FUSION_A = 'em_fusion_a'
    RENDER_STACK_FUSION_B = 'em_fusion_b'

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
    def register_adjacent_stacks(cls, chnk):
        return {
            'stack_a': cls.register_adjacent_stack_a(chnk),
            'stack_b': cls.register_adjacent_stack_b(chnk)
        }
