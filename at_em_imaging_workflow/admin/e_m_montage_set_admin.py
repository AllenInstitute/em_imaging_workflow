from django.contrib import admin
from development.models import state_machines
from django.urls import reverse
from django.utils.safestring import mark_safe


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


class EMMontageSetAdmin(admin.ModelAdmin):
    change_list_template = 'admin/em_montage_set_change_list.html'
    list_display = [
        'id',
        'specimen_link',
        'microscope_link',
        'z_index',
        'reference_set_link',
        'acquisition_date',
        'workflow_state']
    list_select_related = [
        'microscope',
        'reference_set',
        'section',
        'section__specimen']
    list_filter = [
        'section__specimen__uid',
        'microscope__uid',
        'workflow_state']
    actions = [pass_em_montage_set]

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

    def reference_set_link(self, em_montage_set_object):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:development_referenceset_change",
                    args=(em_montage_set_object.reference_set.pk,)),
            str(em_montage_set_object.reference_set)))

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        return response