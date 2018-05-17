from django.contrib import admin
from development.models import state_machines


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
    list_display = [
        'id',
        'specimen',
        'microscope',
        'z_index',
        'reference_set',
        'acquisition_date',
        'workflow_state']
    list_select_related = [
        'microscope',
        'reference_set',
        'section']
    list_filter = [
        'section__specimen__uid',
        'microscope__uid',
        'workflow_state']
    actions = [pass_em_montage_set]
