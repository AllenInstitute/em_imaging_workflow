from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from workflow_engine.models.configuration import Configuration
from django.contrib.contenttypes.models import ContentType
from development.models import state_machines
from django.urls import reverse
from django.utils.safestring import mark_safe
from workflow_engine.models.well_known_file import WellKnownFile
from development.models.e_m_montage_set import EMMontageSet
import simplejson as json
from development.models.chunk import Chunk


def redo_point_match(modeladmin, request, queryset):
    pass_em_montage_set.short_description = \
        "Pass selected montage sets"

    if queryset:
        for em_mset in queryset.iterator():
            state_machines.transition(
                em_mset,
                'workflow_state',
                state_machines.states(EMMontageSet).REDO_POINT_MATCH)
            em_mset.save()

def redo_solver(modeladmin, request, queryset):
    pass_em_montage_set.short_description = \
        "Pass selected montage sets"

    if queryset:
        for em_mset in queryset.iterator():
            state_machines.transition(
                em_mset,
                'workflow_state',
                state_machines.states(EMMontageSet).REDO_SOLVER)
            em_mset.save()

def pass_em_montage_set(modeladmin, request, queryset):
    pass_em_montage_set.short_description = \
        "Pass selected montage sets"

    if queryset:
        for em_mset in queryset.iterator():
            state_machines.transition(
                em_mset,
                'workflow_state',
                state_machines.states(EMMontageSet).MONTAGE_QC_PASSED)
            em_mset.save()

def fail_em_montage_set(modeladmin, request, queryset):
    fail_em_montage_set.short_description = \
        "FAIL selected montage sets"

    if queryset:
        for em_mset in queryset.iterator():
            state_machines.transition(
                em_mset,
                'workflow_state',
                state_machines.states(EMMontageSet).FAILED)
            em_mset.save()


def assign_chunk(modeladmin, request, queryset):
    for em_mset in queryset:
        Chunk.assign_montage_set_to_chunks(em_mset)


class ConfigurationInline(GenericStackedInline):
    model = Configuration


class WellKnownFileInline(GenericStackedInline):
    model = WellKnownFile


class EMMontageSetAdmin(admin.ModelAdmin):
    change_list_template = 'admin/em_montage_set_change_list.html'
    list_display = [
        'id',
        'z_index',
        'qc_link',
        'specimen_link',
        'microscope_link',
        'reference_set_link',
        'acquisition_date',
        'workflow_state',
        'load_uid'
    ]
    list_select_related = [
        'microscope',
        'reference_set',
        'section',
        'section__specimen',
        'sample_holder',
        'sample_holder__load',
    ]
    list_filter = [
        'section__specimen__uid',
        'microscope__uid',
        'workflow_state',
        'sample_holder__load'
    ]
    actions = [
        assign_chunk,
        redo_point_match,
        redo_solver,
        pass_em_montage_set,
        fail_em_montage_set
    ]
    inlines = (ConfigurationInline,)

    def load_uid(self, em_montage_set_object):
        try:
            l = em_montage_set_object.sample_holder.load
        except:
            return ''

        if l:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:development_load_change",
                        args=(l.pk,)),
                str(l.uid)))

    def microscope_link(self, em_montage_set_object):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:development_microscope_change",
                    args=(em_montage_set_object.microscope.pk,)),
            str(em_montage_set_object.microscope)))

    def specimen_link(self, em_montage_set_object):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:development_specimen_change",
                    args=(em_montage_set_object.section.specimen.pk,)),
            str(em_montage_set_object.section.specimen)))

    specimen_link.short_description = "Specimen"


    def qc_link(self, em_montage_set_object):
        try:
            em_mset_type = ContentType.objects.get_for_model(
                EMMontageSet)
            wkf = WellKnownFile.objects.filter(
                attachable_type=em_mset_type,
                attachable_id=em_montage_set_object.id,
                well_known_file_type='defect_detection').first()
            filename = str(wkf)

            with open(filename) as j:
                json_data = json.loads(j.read())
                url = 'file:////' + json_data['output_html'][0]
            text = 'Plot'
        except:
            url = ''
            text = '-'

        return mark_safe('<a target="qc" href="{}">{}</a>'.format(url, text))


    def reference_set_link(self, em_montage_set_object):
        try:
            pk = em_montage_set_object.reference_set.pk
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:development_referenceset_change",
                        args=(pk,)),
                str(em_montage_set_object.reference_set)))
        except:
            return ''


    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        return response
