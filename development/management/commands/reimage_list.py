from django.core.management.base import BaseCommand
from development.models.e_m_montage_set import EMMontageSet

class Command(BaseCommand):
    help = 'list montage sets for reimage'

    def add_arguments(self, parser):
        parser.add_argument(
             '--min_z',
            help="Montage sets will be reassigned from this reference set")
        parser.add_argument(
             '--max_z',
            help="Montage sets will be reassigned to this reference set")

    def handle(self, *args, **options):
        min_z = options.get('min_z', None)
        max_z = options.get('max_z', None)

        print("{} -> {}".format(min_z, max_z))

        em_msets = EMMontageSet.objects.filter(
            section__z_index__gte=min_z,
            section__z_index__lte=max_z)

        for m in sorted(em_msets, key=lambda em: em.section.z_index):
            print(m)
