from django.contrib import admin
from django.forms import ModelForm
from django.contrib.contenttypes.admin import GenericStackedInline
from workflow_engine.workflow_controller import WorkflowController
from workflow_engine.models.configuration import Configuration
from django.urls import reverse
from django.utils.safestring import mark_safe
from development.models.e_m_montage_set import EMMontageSet


def redo_lens_correction(modeladmin, request, queryset):
    redo_lens_correction.short_description = \
        "Redo lens correction"

    if queryset:
        for refset in queryset.iterator():
            refset.redo()
            refset.save()

            WorkflowController.start_workflow(
                'em_2d_montage',
                refset,
                start_node_name='Generate Lens Correction Transform',
                reuse_job=True,
                raise_priority=True)


class LensCorrectionConfigurationForm(ModelForm):
    class Meta:
        model=Configuration
        fields=(
            'name',
            'configuration_type',
            'json_object',)

    def clean_configuration_type(self):
        ct = self.cleaned_data.get('configuration_type', None)

        return ct

    def clean_json_object(self):
        jo = self.cleaned_data.get('json_object', {})

        return jo


class ConfigurationInline(GenericStackedInline):
    model = Configuration
    form=LensCorrectionConfigurationForm
    extra=0


class EMMontageInline(admin.StackedInline):
    model = EMMontageSet
    #fk_name = "reference_set"
    extra = 0


def set_refset_to_pending(modeladmin, request, queryset):
    set_refset_to_pending.short_description = \
        "Set to PENDING"

    if queryset:
        for refset in queryset.iterator():
            refset.reset_pending()
            refset.save()


def set_refset_to_done(modeladmin, request, queryset):
    set_refset_to_done.short_description = \
        "Set to DONE"

    if queryset:
        for refset in queryset.iterator():
            refset.finish_processing()
            refset.save()

class ReferenceSetAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/em_montage_set_change_list.html'
    list_display = [
        'id',
        'object_state',
        'microscope_link',
        'manifest_path',
        'acquisition_date',
    ]
    search_fields = (
        'id',
    )
    list_select_related = [
        'microscope'
    ]
    list_filter = [
        'microscope__uid',
        'object_state'
    ]
    actions = [
        set_refset_to_pending,
        set_refset_to_done,
        redo_lens_correction
    ]
    inlines = (ConfigurationInline, )#EMMontageInline)

    def microscope_link(self, em_montage_set_object):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:development_microscope_change",
                    args=(em_montage_set_object.microscope.pk,)),
            str(em_montage_set_object.microscope)))

    microscope_link.short_description = "Microscope"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        return response
