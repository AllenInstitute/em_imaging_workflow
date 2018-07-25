from django.contrib import admin
from development.models.section import Section


class ChunkInline(admin.StackedInline):
    model = Section.chunks.through
    extra=0


class SectionAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/_change_list.html'
    list_display = [
        'section_id',
        'z_index',
        'metadata',
        'specimen'
        ]
    list_select_related = []
    list_filter = []
    actions = []
    inlines = [ChunkInline,]
