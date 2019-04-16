from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.forms import (
    Form,
    IntegerField,
    CharField
)
from at_em_imaging_workflow.models import (
    EMMontageSet,
    Section,
    SampleHolder
)
from datetime import datetime
import uuid


def create_gap_section_handler(z_index, reimage_index, gap_z_index):
    msets = EMMontageSet.objects.filter(
        section__z_index=gap_z_index) 
    
    if len(msets) != 0:
        raise Exception(
            'Montage set for {} already exists'.format(
                gap_z_index))


    em_mset_to_copy = EMMontageSet.objects.filter(
        section__z_index=z_index
    ).order_by(
        'id'
    )[
        reimage_index
    ]

    gap_section,_ = Section.objects.update_or_create(
        z_index=gap_z_index,
        specimen = em_mset_to_copy.section.specimen,
        defaults={ 'metadata': None }
    )

    gap_sample_holder,_ = SampleHolder.objects.update_or_create(
        uid='gap {}'.format(gap_z_index),
        load=em_mset_to_copy.sample_holder.load,
        defaults={ 'imaged_sections_count': 0 }
    )

    gap_em_montage_set = EMMontageSet.objects.create(
        uid=uuid.uuid4(),
        acquisition_date=datetime.now(),
        overlap=0,
        object_state=EMMontageSet.STATE.EM_MONTAGE_SET_GAP,
        mipmap_directory="",
        section=gap_section,
        sample_holder=gap_sample_holder,
        reference_set=None,
        reference_set_uid="",
        storage_directory=None,
        metafile=None,
        camera=em_mset_to_copy.camera,
        microscope=em_mset_to_copy.microscope
    )

    return gap_em_montage_set


class CreateGapSectionForm(Form):
    z_index = IntegerField()
    reimage_index = IntegerField()
    gap_z_index = IntegerField()

    def do_create(self):
        return create_gap_section_handler(
            self.cleaned_data['z_index'],
            self.cleaned_data['reimage_index'],
            self.cleaned_data['gap_z_index'])


class CreateGapSectionView(FormView):
    template_name = 'create_gap_section.html'
    form_class = CreateGapSectionForm
    success_url = reverse_lazy(
        'admin:at_em_imaging_workflow_emmontageset_changelist')

    def form_valid(self, form):
        form.do_create()
        return super().form_valid(form)
