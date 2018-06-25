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


def pass_em_montage_set(modeladmin, request, queryset):
    pass_em_montage_set.short_description = \
        "Pass selected montage sets"

    if queryset:
        for em_mset in queryset.iterator():
            state_machines.transition(
                em_mset,
                'workflow_state',
                state_machines.states(em_mset).montage_qc_passed)
            em_mset.save()


def redo_point_match(modeladmin, request, queryset):
    pass


def redo_solver(modeladmin, request, queryset):
    pass


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
        'specimen_link',
        'microscope_link',
        'z_index',
        'reference_set_link',
        'acquisition_date',
        'workflow_state',
        'qc_link']
    list_select_related = [
        'microscope',
        'reference_set',
        'section',
        'section__specimen']
    list_filter = [
        'section__specimen__uid',
        'microscope__uid',
        'workflow_state']
    actions = [
        assign_chunk,
        redo_point_match,
        redo_solver,
        pass_em_montage_set
    ]
    inlines = (ConfigurationInline,)

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
                url = 'file:////' + json_data['output_html']
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
