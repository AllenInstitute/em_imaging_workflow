from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.admin import GenericStackedInline
from workflow_engine.models.configuration import Configuration
from development.models import state_machines
from django.urls import reverse
from django.utils.safestring import mark_safe
from workflow_engine.models.well_known_file import WellKnownFile
from development.models.e_m_montage_set import EMMontageSet
import simplejson as json
from development.models.chunk import Chunk
from development.strategies.generate_mesh_lens_correction \
    import GenerateMeshLensCorrection


class LensCorrectionConfigurationForm(ModelForm):
    class Meta:
        model=Configuration
        fields=(
            'name',
            'configuration_type',
            'json_object',)

    def clean_configuration_type(self):
        ct = self.cleaned_data.get('configuration_type', None)

        if ct is None:
            raise ValidationError("Invalid configuration type")
        elif GenerateMeshLensCorrection.CONFIGURATION_TYPE != ct:
            raise ValidationError("Configuration type must be {}".format(
                GenerateMeshLensCorrection.CONFIGURATION_TYPE))

        return ct

    def clean_json_object(self):
        jo = self.cleaned_data.get('json_object', {})

        if jo is None:
            raise ValidationError("Invalid JSON object")
        elif GenerateMeshLensCorrection.TRANSFORM not in jo:
            raise ValidationError("Must specify {}".format(
                GenerateMeshLensCorrection.TRANSFORM))
        else:
            jo['cleaned'] = True

        return jo


class ConfigurationInline(GenericStackedInline):
    model = Configuration
    form=LensCorrectionConfigurationForm
    max_num=1


#class WellKnownFileInline(GenericStackedInline):
#    model = WellKnownFile

def set_refset_to_pending(modeladmin, request, queryset):
    set_refset_to_pending.short_description = \
        "Set to PENDING"

    if queryset:
        for refset in queryset.iterator():
            refset.workflow_state = 'PENDING'
            refset.save()

class ReferenceSetAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/em_montage_set_change_list.html'
    list_display = [
        'id',
        'workflow_state',
        'microscope_link',
        'manifest_path',
        'acquisition_date',
    ]
    list_select_related = [
        'microscope'
    ]
    list_filter = [
        'microscope__uid',
        'workflow_state'
    ]
    actions = [
        set_refset_to_pending,
    ]
    inlines = (ConfigurationInline,)

    def microscope_link(self, em_montage_set_object):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:development_microscope_change",
                    args=(em_montage_set_object.microscope.pk,)),
            str(em_montage_set_object.microscope)))

    microscope_link.short_description = "Microscope"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        return response
