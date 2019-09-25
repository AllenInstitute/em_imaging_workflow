import pytest
from mock import patch, Mock
from at_em_imaging_workflow.models import ReferenceSet
from at_em_imaging_workflow.strategies.montage.generate_mesh_lens_correction import (
    GenerateMeshLensCorrection
)
from datetime import datetime
from at_em_imaging_workflow.models import Microscope
from django.test.utils import override_settings

mock_temca3_template = {
  "rerun_pointmatch": True,
  "match_collection": "em_2d_lens_matches",
  "metafile": "/allen/programs/celltypes/production/wijem/incoming_data/17797_1R_Tape162_TEMCA3_05_20180716142023_reference_0/_metadata_20180716142023_17797_1R_Tape162_TEMCA3_05_20180716142023_reference_0_.json",
  "z_index": 5921,
  "output_dir": "/allen/programs/celltypes/workgroups/em-connectomics/danielk/masks_for_stacks/test_50M_data/out",
  "outfile": "/allen/programs/celltypes/workgroups/em-connectomics/danielk/masks_for_stacks/test_50M_data/out/lens_correction_out.json",
  "ncpus": -1,
  "log_level": "ERROR",
  "close_stack": True,
  "input_stack": "em_2d_raw_lc_stack",
  "render": {
    "client_scripts": "/allen/aibs/pipeline/image_processing/volume_assembly/render-jars/production/scripts",
    "host": "em-131db",
    "project": "em_2d_montage_staging",
    "memGB": "5G",
    "owner": "danielk",
    "port": 8080
  },
  "nvertex": 2000,
  "regularization": {
    "default_lambda": 100000.0,
    "lens_lambda": 1e-05,
    "log_level": "ERROR",
    "translation_factor": 1e-05
  },
  "overwrite_zlayer": True,
  "output_stack": "em_2d_lc_corrected",
  "ndiv": 25,
  "matchMax": 20000,
  "downsample_scale": 0.5,
  "SIFT_nfeature": 100000,
  "SIFT_noctave": 8,
  "SIFT_sigma": 2.5,
  "RANSAC_outlier": 5.0,
  "FLANN_ntree": 5,
  "FLANN_checks": 50,
  "ratio_of_dist": 0.7,
  "CLAHE_grid": 16,
  "CLAHE_clip": 2.5,
  "mask_coords": [[0, 300], [500, 0], [5504, 0], [5504, 5504], [0, 5504]],
  "mask_dir": "/allen/programs/celltypes/workgroups/em-connectomics/danielk/masks_for_stacks",
  "ncpus": -1
}

@pytest.mark.django_db
@override_settings(
    RENDER_SERVICE_URL='http://render.example.org',
    RENDER_SERVICE_PORT=1234
    #FIJI_PATH='/path/to/fiji'
)
def test_get_input_data():
    enqueued_object = ReferenceSet(
        uid='deadbeef',
        manifest_path='manifest.json',
        microscope=Microscope(uid='temca2'),
        project_path='/path/to/project')

    storage_directory = '/example/storage/directory'
    mock_task = Mock()

    strategy = GenerateMeshLensCorrection()
    with patch('at_em_imaging_workflow.strategies.montage.'
               'generate_mesh_lens_correction.GenerateMeshLensCorrection.'
               'get_workflow_node_input_template',
               Mock(return_value=mock_temca3_template)):
        inp = strategy.get_input(enqueued_object,
                                 storage_directory,
                                 mock_task)

    assert inp is not None

    assert inp['render']['host'] == 'http://render.example.org'
    assert inp['render']['port'] == 1234

    # TODO: ok per DanK, but parametrize this
    assert inp['render']['project'] == 'em_2d_montage_staging'


@pytest.mark.django_db
def test_on_failure():
    ref_set = ReferenceSet(
        uid='deadbeef',
        manifest_path='manifest.json',
        project_path='/path/to/project',
        object_state=ReferenceSet.STATE.LENS_CORRECTION_PROCESSING)
    task = Mock()
    task.enqueued_task_object = ref_set

    strategy = GenerateMeshLensCorrection()
    strategy.on_failure(task)

    assert ref_set.object_state == ReferenceSet.STATE.LENS_CORRECTION_PENDING

@pytest.mark.django_db
def test_on_finishing():
    ref_set = ReferenceSet(
        uid='deadbeef',
        manifest_path='manifest.json',
        project_path='/path/to/project',
        acquisition_date=datetime.now(),
        object_state=ReferenceSet.STATE.LENS_CORRECTION_PROCESSING)
    task = Mock()
    task.enqueued_task_object = ref_set

    strategy = GenerateMeshLensCorrection()

#     with patch.object(strategy, 'set_well_known_file') as swkf_mock:
    results = {
        'output_json': 'mock_out',
        'maskUrl': 'http://example.org/mask/url.html'
    }
    strategy.on_finishing(ref_set, results, task)

    assert ref_set.object_state == ReferenceSet.STATE.LENS_CORRECTION_DONE
#     swkf_mock.assert_not_called()
