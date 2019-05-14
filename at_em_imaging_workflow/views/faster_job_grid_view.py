from django.http import JsonResponse
from at_em_imaging_workflow.faster_job_grid import FasterJobGrid

def faster_job_grid(request):
    tape = request.GET.get('tape', None)
    z_min = int(request.GET.get('z_min', None))
    z_max = int(request.GET.get('z_max', None))
    fjg = FasterJobGrid(
        tape,
        (z_min, z_max),
        [
            "Ingest Tile Sets",
            "Generate Lens Correction Transform",
            "Generate Render Stack",
            "Generate MIPMaps",
            "Apply MIPMaps",
            "Wait for Lens Correction",
            "Apply Lens Correction",
            "Create Tile Pairs",
            "2D Montage Point Match",
            "2D Montage Python Solver",
            "Detect Defects",
            "Manual QC / High Degree Polynomial or Point Match Regeneration",
            "Load Z Mapping",
            "Chunk Assignment",
            "Wait for Z Mapping",
            "Make Montage Scapes",
            "Remap Zs",
            "Wait for Chunk Assignment",
            "Wait for Complete Chunk",
            "Create Rough Tile Pairs",
            "EM Rough Point Match",
            "Rough Align Python Solver",
            "Rough Align Python Solver 2",
            "Rough Align Manual QC",
            "Apply Rough Alignment",
            "Register Adjacent Stack",
            "Fuse Stacks",
            "Rough Alignment Materialize"
        ]
    )
    return JsonResponse(fjg.get_dict())