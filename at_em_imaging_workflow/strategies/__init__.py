#
# TODO: replace w/ stack manager
#
#RENDER_STACK_INGEST = 'em_2d_montage_ingest'
#RENDER_STACK_LENS_CORRECTED = 'em_2d_montage_lc'
RENDER_STACK_MESH_LENS_RAW = 'em_2d_raw_lc_stack'
RENDER_STACK_MESH_LENS_CORRECTED = 'em_2d_lc_corrected'
RENDER_LENS_COLLECTION = 'em_2d_lens_matches'
#RENDER_STACK_APPLY_MIPMAPS = 'em_2d_montage_apply_mipmaps'
RENDER_STACK_TILE_PAIRS = 'em_2d_montage_tile_pairs'
RENDER_STACK_POINT_MATCH = 'em_2d_montage_point_match'
RENDER_STACK_SOLVED = 'em_2d_montage_solved'
RENDER_STACK_SOLVED_PYTHON = 'em_2d_montage_solved_py'
RENDER_STACK_REDIRECT_MIPMAPS = 'em_2d_montage_redirect_mipmaps'
#RENDER_STACK_DOWNSAMPLED = 'em_2d_montage_downsampled_no_scale_z_mapped'
RENDER_STACK_DOWNSAMPLED = 'em_2d_montage_solved_py_0_01_mapped'
# RENDER_STACK_DOWNSAMPLED_UNMAPPED = 'em_2d_montage_downsampled_no_scale_no_mapping'
RENDER_STACK_DOWNSAMPLED_UNMAPPED = 'em_2d_montage_downsampled_no_mapping'

# ROUGH ALIGN
# string interpolation values are zmin, zmax
RENDER_STACK_RIGID_ALIGN_DOWNSAMPLE = \
    'em_rigid_align_solved_downsample_zs%d_ze%d'
RENDER_STACK_ROUGH_ALIGN_DOWNSAMPLE = \
    'em_rough_align_solved_downsample_zs%d_ze%d'
RENDER_STACK_MONTAGE_SCAPES_STACK = \
    'em_montage_scapes_zs_%d_ze_%d'
RENDER_STACK_ROUGH_ALIGN = 'em_rough_align_zs%d_ze%d'
RENDER_STACK_ROUGH_SOLVED = 'em_rough_align_zs%d_ze%d_solved'
