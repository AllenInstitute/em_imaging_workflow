from django.contrib import admin


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

    @classmethod
    def pass_em_montage_set(cls, modeladmin, request, queryset):
        queryset.update(workflow_status="MONTAGE_QC_PASSED")
    
    pass_em_montage_set.short_description = \
        "Pass selected montage sets"
    actions = [pass_em_montage_set]