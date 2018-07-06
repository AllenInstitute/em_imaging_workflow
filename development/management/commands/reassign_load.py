from django.core.management.base import BaseCommand
from development.models.e_m_montage_set import EMMontageSet
from development.models.load import Load
from development.models.reference_set import ReferenceSet
from development.models.section import Section
from development.models.sample_holder import SampleHolder
from workflow_engine.models.job import Job
from django.db.models import F

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
             '--load',
            help="Load name")
        parser.add_argument(
             '--new_load',
            help="New Load name")

    def handle(self, *args, **options):
        load_name = options.get('load', None)
        new_load_name = options.get('new_load', None)

        try:
            load = Load.objects.get(
                uid=load_name)
            print("Load: {}".format(
                str(load)))
        except:
            print("error finding load")

        try:
            new_load = Load.objects.get(
                uid=new_load_name)
            print("New Load: {}".format(
                str(new_load)))
        except:
            print("error finding new load")

        try:
            msets = EMMontageSet.objects.filter(
                sample_holder__load=load,
                section__z_index__lt=300)

            for mset in msets:
                try:
                    sctn_140 = Section.objects.get(
                        z_index=mset.section.z_index + 140000)
                    mset.section=sctn_140
                    mset.save()
                    print('found duplicate section: {}'.format(str(sctn_140)))
                except:
                    mset.section.z_index=mset.section.z_index + 140000
                    mset.section.save()
                    print('updated section: {}'.format(str(mset.section)))
                try:
                    smpl_hldr = mset.sample_holder
                    smpl_hldr.load = new_load
                    smpl_hldr.save()
                    print('updated sample holder {}'.format(
                        str(smpl_hldr)))
                except:
                    print('could not update sample holder {}'.format(
                        str(smpl_hldr)))
        except Exception as e:
            print(str(e))

