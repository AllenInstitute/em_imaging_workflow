from django.contrib import admin
from at_em_imaging_workflow.models import SampleHolder, Load


class LoadInline(admin.StackedInline):
    model = Load


class SampleHolderAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/_change_list.html'
    list_display = [
        'uid',
        'imaged_sections_count',
        'load'
        ]
    list_select_related = ['load']
    list_filter = ['load']
    actions = []
    inlines = []
