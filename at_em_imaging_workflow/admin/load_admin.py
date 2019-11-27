from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from workflow_engine.models import Configuration
from django.contrib.contenttypes.admin import GenericStackedInline
from at_em_imaging_workflow.models import Chunk, Load
from .create_chunk_form import CreateChunkForm
from .z_mapping_form import ZMappingForm
import logging

class LoadConfigurationForm(ModelForm):
    class Meta:
        model=Configuration
        fields=('name','configuration_type', 'json_object')
        extra=0
        _log = logging.getLogger('at_em_imaging_workflow.admin.load_admin')

    def __init__(self, *args, **kwargs):
        LoadConfigurationForm._log.debug('LoadConfigurationForm')

        super(LoadConfigurationForm, self).__init__(*args, **kwargs)


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
    _log = logging.getLogger('at_em_imaging_workflow.admin.load_admin')

    def __init__(self, *args, **kwargs):
        LoadConfigurationInline._log.debug('LoadConfigurationInline')

        super(LoadConfigurationInline, self).__init__(*args, **kwargs)


class ChunkInline(admin.StackedInline):
    model = Chunk
    form=CreateChunkForm
    extra=0
    _log = logging.getLogger('at_em_imaging_workflow.admin.load_admin')

class ZMappingInline(GenericStackedInline):
    model = Configuration
    form=ZMappingForm
    verbose_name = "Z Mapping"
    verbose_name_plural = "Z Mappings"
    extra=0
    max_num = 1

    def get_fields(self, request, load_obj=None):
        if (load_obj and load_obj.object_state == "PENDING"):
            return ('xls_path',)
        else:
            return ('name', 'json_object')

class LoadForm(ModelForm):
    _log = logging.getLogger('at_em_imaging_workflow.admin.load_admin')

    class Meta:
        model = Load
        fields = "__all__"

    def save(self, commit=True):
        LoadForm._log.info("Save Load Form: {}".format(commit))
        return super(LoadForm, self).save(commit)


class LoadAdmin(admin.ModelAdmin):
    form = LoadForm
    list_display = [
        'uid',
        'offset'
    ]
    list_select_related = []
    list_filter = []
    actions = []
    inlines = (ZMappingInline, ChunkInline,)
    _log = logging.getLogger('at_em_imaging_workflow.admin.load_admin')

    def save_form(self, request, form, change):
        LoadAdmin._log.info('SAVE FORM {}'.format(change))
        return super(LoadAdmin, self).save_form(request, form, change)

    def save_formset(self, request, form, formset, change):
        LoadAdmin._log.info('SAVE FORMSET {}'.format(change))
        return super(LoadAdmin, self).save_formset(request, form, formset, change)

#     def save_model(self, request, obj, form, change):
#         LoadAdmin._log.info('SAVE MODEL')
#         raise Exception("I am sad")
#         return super(LoadAdmin, self).save_model(request, obj, form, change)
# 
#     def save_related(self, request, obj, form, formsets, change):
#         raise Exception("I am sad 2")
#         LoadAdmin._log.info('SAVE RELATED')
#         return super(LoadAdmin, self).save_related(request, form, formsets, change)