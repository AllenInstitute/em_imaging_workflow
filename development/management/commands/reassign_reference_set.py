from django.core.management.base import BaseCommand
from development.models.e_m_montage_set import EMMontageSet
from development.models.reference_set import ReferenceSet
from workflow_engine.models.job import Job

archive_workflow_nodes = [
    "Apply Lens Correction",
    "Create Tile Pairs",
    "2D Montage Point Match",
    "2D Montage Python Solver",
    "Detect Defects",
    "Manual QC / High Degree Polynomial or Point Match Regeneration",
    "Generate Downsampled Montage",
    "Make Montage Scapes",
    "Chunk Assignment"
]

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
             '--failed_reference_set',
            help="Montage sets will be reassigned from this reference set")
        parser.add_argument(
             '--replacement_reference_set',
            help="Montage sets will be reassigned to this reference set")

    def handle(self, *args, **options):
        failed_refset_id = options.get('failed_reference_set', None)
        replacement_refset_id = options.get('replacement_reference_set', None)

        try:
            failed_refset = ReferenceSet.objects.get(
                id=failed_refset_id)
            print("Failed refset: {}".format(
                str(failed_refset)))
        except:
            print("error finding failed refset")

        if failed_refset.workflow_state != 'FAILED':
            print("Failed refset is not in the FAILED workflow state.")
            return

        print("Reassigning EM montage sets")

        try:
            replacement_refset = ReferenceSet.objects.get(
                id=replacement_refset_id)
            print("Replacement refset: {}".format(
                str(replacement_refset)))
        except:
            print("error finding replacement refset")

        updated = False
        msets_to_move = EMMontageSet.objects.filter(
            reference_set=failed_refset)
        updated = msets_to_move.update(
            reference_set=replacement_refset)

        if updated:
            print("Montage sets moved")
        else:
            print("Failed to move montage sets")

        for mset in msets_to_move:
            print(str(mset))
        
