from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from workflow_engine.models import Configuration
from django.contrib.contenttypes.admin import GenericStackedInline
from at_em_imaging_workflow.models import Chunk
from .create_chunk_form import CreateChunkForm
from .z_mapping_form import ZMappingForm

class LoadConfigurationForm(ModelForm):
    class Meta:
        model=Configuration
        fields=('name','configuration_type', 'json_object')
        extra=0

    def clean_json_object(self):
        jo = self.cleaned_data.get('json_object', {})

        if jo is None:
            raise ValidationError("Invalid JSON object")

        return jo

    def clean_configuration_type(self):
        config_type = self.cleaned_data.get('configuration_type', 'z_mapping')

        #if 'z_mapping' != config_type:
        #    raise ValidationError("Only z_mapping configurations allowed")

        return config_type

    def clean_name(self):
        name = self.cleaned_data.get(
            'name', 'Z Mapping')

        if name is None:
            raise ValidationError("Need a name")

        return name


class LoadConfigurationInline(GenericStackedInline):
    model=Configuration
    form=LoadConfigurationForm
    extra=0


class ChunkInline(admin.StackedInline):
    model = Chunk
    form=CreateChunkForm
    extra=0

class ZMappingInline(GenericStackedInline):
    model = Configuration
    form=ZMappingForm
    verbose_name = "Z Mapping"
    verbose_name_plural = "Z Mappings"
    extra=0
    max_num = 1


class LoadAdmin(admin.ModelAdmin):
    list_display = [
        'uid',
        'offset'
    ]
    list_select_related = []
    list_filter = []
    actions = []
    inlines = (ZMappingInline, ChunkInline,)
