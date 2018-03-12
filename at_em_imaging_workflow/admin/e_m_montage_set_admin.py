from django.contrib import admin


def pass_em_montage_set(modeladmin, request, queryset):
    pass_em_montage_set.short_description = \
        "Pass selected montage sets"

    queryset.update(workflow_status="MONTAGE_QC_PASSED")


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
