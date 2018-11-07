from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from workflow_engine.models.configuration import (
    Configuration,
)
from django.contrib.contenttypes.admin import GenericStackedInline


class RenderedVolumeConfigurationForm(ModelForm):
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


class RenderedVolumeConfigurationInline(GenericStackedInline):
    model=Configuration
    form=RenderedVolumeConfigurationForm
    extra=0


class RenderedVolumeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'mipmap_directory',
        'specimen')
    list_select_related = ()
    list_filter = ()
    actions = ()
    inlines = [RenderedVolumeConfigurationInline]
