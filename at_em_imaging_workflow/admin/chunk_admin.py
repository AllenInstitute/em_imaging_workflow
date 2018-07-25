from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from workflow_engine.models.configuration \
    import Configuration
from django.contrib.contenttypes.admin import GenericStackedInline
from django.urls import reverse
from django.utils.safestring import mark_safe


class ChunkConfigurationForm(ModelForm):
    class Meta:
        model=Configuration
        fields=('name', 'configuration_type', 'json_object',)
        extra=0

    def clean_json_object(self):
        jo = self.cleaned_data.get('json_object', {})

        if jo is None:
            raise ValidationError("Invalid JSON object")
        else:
            pass

        return jo


class ChunkConfigurationInline(GenericStackedInline):
    model=Configuration
    form=ChunkConfigurationForm
    max_num=1


def remap_chunk(modeladmin, request, queryset):
    pass

def initialize_z_mapping(modeladmin, request, queryset):
    for chnk in queryset:
        z_mapping = { z: z for z in chnk.z_list() }
        z_mapping, _ = chnk.configurations.update_or_create(
            configuration_type='z_mapping',
            defaults={
                'name': 'chunk {} z mapping'.format(chnk.computed_index),
                'json_object': z_mapping
            })


class ChunkAdmin(admin.ModelAdmin):
    change_list_template = 'admin/chunk_change_list.html'
    list_display = [
        'id',
        'computed_index',
        'chunk_state',
        'rendered_volume',
        'preceding_link',
        'following_link']
    list_select_related = []
    list_filter = []
    actions = [initialize_z_mapping, remap_chunk]
    inlines = [ChunkConfigurationInline]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        return response

    def preceding_link(self, chunk_object):
        c = chunk_object.chunk_preceding_chunk.first()

        if c:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:development_chunk_change",
                        args=(c.pk,)),
                str(c)))
        else:
            return mark_safe('<div />')

    preceding_link.short_description = 'preceding chunk'


    def following_link(self, chunk_object):
        c = chunk_object.chunk_following_chunk.first()

        if c:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:development_chunk_change",
                        args=(c.pk,)),
                str(c)))
        else:
            return mark_safe('<div />')

    following_link.short_description = 'following chunk'
