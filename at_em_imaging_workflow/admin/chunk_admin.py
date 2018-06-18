from django.contrib import admin
from development.models.chunk import Chunk


class SectionInline(admin.StackedInline):
    model = Chunk.sections.through


class ChunkAdmin(admin.ModelAdmin):
    change_list_template = 'admin/chunk_change_list.html'
    list_display = [
        'id',
        'computed_index',
        'chunk_state',
        'rendered_volume',
        'preceding_chunk',
        'following_chunk',
        ]
    list_select_related = []
    list_filter = []
    actions = []
    inlines = [SectionInline,]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        return response