from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
#from django.contrib.contenttypes.forms import generic_inlineformset_factory
from workflow_engine.models.configuration  import Configuration
from workflow_engine.workflow_controller import WorkflowController
from development.strategies.rough.solve_rough_alignment_strategy import (
    SolveRoughAlignmentStrategy as SRAS
)
from development.models.section import Section
from django.contrib.contenttypes.admin import GenericStackedInline
from django.urls import reverse
from django.utils.safestring import mark_safe

def qc_pass_chunk(modeladmin, request, queryset):
    qc_pass_chunk.short_description = \
        "QC Pass selected chunks"

    if queryset:
        for chnk in queryset.iterator():
            chnk.rough_qc_pass()
            chnk.save()

        WorkflowController.enqueue_next_queue_by_workflow_node(
            'rough_align_em_2d',
            chnk,
            start_node_name='Rough Align Manual QC')

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
    extra=0


def remap_chunk(modeladmin, request, queryset):
    pass


def update_chunk_assignment(c):
    chunk_load = c.get_load()
    z_mapping = chunk_load.get_z_mapping()
    tile_pair_ranges = c.get_tile_pair_ranges()
    min_z, max_z = SRAS.calculate_z_min_max(tile_pair_ranges)
    clipped_z_mapping = SRAS.clip_z_mapping_to_min_max(
        z_mapping, min_z, max_z) 
    cas = c.chunkassignment_set.all()
    temp_zs = [int(k) for k in clipped_z_mapping.keys()]
    bad_cas = c.chunkassignment_set.all().exclude(
        section__z_index__in=temp_zs)
    # TODO: delete bad cas
    already_assigned = [ca.section.z_index for ca in cas]
    new_assignments = set(temp_zs) - set(already_assigned)

    for temp_z in new_assignments:
        try:
            assigned_section = Section.objects.get(
                z_index=temp_z)
            new_ca, _ = c.chunkassignment_set.get_or_create(
                chunk=c,
                section=assigned_section)
        except:
            pass

def update_chunk_assignments(modeladmin, request, queryset):
    for chnk in queryset:
        update_chunk_assignment(chnk)
        

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
        'object_state',
        'rendered_volume',
        'preceding_link',
        'following_link',
        'zs']
    list_select_related = []
    list_filter = []
    actions = [
        initialize_z_mapping,
        update_chunk_assignments,
        qc_pass_chunk
    ]
    inlines = [ChunkConfigurationInline]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        return response

    def preceding_link(self, chunk_object):
        c = chunk_object.preceding_chunk

        if c:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:development_chunk_change",
                        args=(c.pk,)),
                str(c)))
        else:
            return mark_safe('<div />')

    preceding_link.short_description = 'preceding chunk'


    def following_link(self, chunk_object):
        c = chunk_object.following_chunk

        if c:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:development_chunk_change",
                        args=(c.pk,)),
                str(c)))
        else:
            return mark_safe('<div />')

    following_link.short_description = 'following chunk'

    def zs(self, chunk_object):
        mapping = chunk_object.get_z_mapping()
        temp_zs = [int(z) for z in mapping.keys()]
        real_zs = mapping.values()

        return "{}-{} ({}-{})".format(
            min(temp_zs),
            max(temp_zs),
            min(real_zs),
            max(real_zs)
        )