from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from at_em_imaging_workflow.models import Chunk
from workflow_engine.models import Configuration
from workflow_engine.workflow_controller import WorkflowController
from at_em_imaging_workflow.models import Section
from django.contrib.contenttypes.admin import GenericStackedInline
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_fsm import can_proceed


def qc_pass_chunk(modeladmin, request, queryset):
    qc_pass_chunk.short_description = \
        "QC Pass selected chunks"

    if queryset:
        for chnk in queryset.iterator():
            if can_proceed(chnk.rough_qc_pass):
                chnk.rough_qc_pass()
                chnk.save()
            else:
                chnk.object_state = Chunk.STATE.CHUNK_ROUGH_QC_PASSED
                chnk.save()

        WorkflowController.enqueue_from_admin_form(
            'rough_align_em_2d',
            'Rough Align Manual QC',
            chnk)

class ChunkConfigurationForm(ModelForm):
    class Meta:
        model=Configuration
        fields=('name', 'content_type', 'configuration_type', 'json_object',)
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
    raise Exception('unimplemented')


def update_chunk_assignment(c):
    z_mapping, min_z, max_z = c.z_info()
    cas = c.chunkassignment_set.all()
    temp_zs = [int(k) for k in z_mapping.keys()]
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

#     def changelist_view(self, request, extra_context=None):
#         response = super().changelist_view(request, extra_context)
# 
#         return response

    def preceding_link(self, chunk_object):
        c = chunk_object.preceding_chunk

        if c:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:at_em_imaging_workflow_chunk_change",
                        args=(c.pk,)),
                str(c)))
        else:
            return mark_safe('<div />')

    preceding_link.short_description = 'preceding chunk'


    def following_link(self, chunk_object):
        c = chunk_object.following_chunk

        if c:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:at_em_imaging_workflow_chunk_change",
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