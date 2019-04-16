from django.contrib import admin
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from workflow_engine.models import Configuration
from django.contrib.contenttypes.admin import GenericStackedInline
from at_em_imaging_workflow.models import Load, Chunk, Section, ChunkAssignment


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

class CreateChunkForm(ModelForm):
    z_min = forms.IntegerField()
    z_max = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.z_min = kwargs.pop('z_min', 0)
        self.z_max = kwargs.pop('z_max', 0)

        super(CreateChunkForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Chunk
        fields=('computed_index', 'chunk_state', 'z_min', 'z_max', 'rendered_volume')
        extra=0

    def clean_computed_index(self):
        ci = self.cleaned_data.get('computed_index', 0)

        if ci == 0:
            raise ValidationError("Invalid computed index")

        return ci

    def clean_z_min(self):
        self.z_min = self.cleaned_data.get('z_min', 0)

        if self.z_min == 0:
            raise ValidationError("Invalid z min")

        return self.z_min

    def clean_z_max(self):
        self.z_max = self.cleaned_data.get('z_max', 0)

        if self.z_max == 0:
            raise ValidationError("Invalid z max")

        return self.z_max

    def clean_rendered_volumme(self):
        rv = self.cleaned_data.get(
            'rendered_volume', '')

        if rv == '':
            raise ValidationError("Invalid rendered volume")

        return rv

    def create_chunk_handler(self, chnk, z_min, z_max):
        load_object = chnk.load
        load_z_mapping = load_object.get_z_mapping()
        chunk_z_mapping = {}
        for z in range(z_min, z_max+1):
            try:
                chunk_z_mapping[str(z)] = load_z_mapping[str(z)]
            except:
                pass

        mapped_min = load_z_mapping[str(z_min)]
        mapped_max = load_z_mapping[str(z_max)]

        chnk_cfg,_ = chnk.configurations.update_or_create(
            configuration_type='chunk_configuration',
            defaults={
                'name': 'Chunk {} {} configuration'.format(
                    chnk.computed_index,
                    chnk.id
                ),
            }
        )
        chnk_cfg.json_object = {
            "tile_pair_ranges": {
                "0": {
                    "maxz": mapped_max,
                    "minz": mapped_min,
                    "tempz": z_min,
                    "zNeighborDistance": 3
                }
            }
        }

        chnk_cfg.save()

        chnk.configurations.update_or_create(
            configuration_type='z_mapping',
            defaults={
                'name': 'Chunk {} {} z_mapping'.format(
                    chnk.computed_index,
                    chnk.id
                ),
                'json_object': chunk_z_mapping
            }
        )

        sections = Section.objects.filter(
            z_index__gte=z_min,
            z_index__lte=z_max)

        cas = []

        for s in sections:
            chnk_assn,_ = ChunkAssignment.objects.get_or_create(
                section=s,
                chunk=chnk
            )

            cas.append(chnk_assn)

        return chnk

    def save(self, commit=True):
        chnk = super(CreateChunkForm, self).save()

        chnk = self.create_chunk_handler(
            chnk,
            self.z_min,
            self.z_max
        )
 
        if commit:
            chnk.save()

        # TODO: enqueue the chunk in wait for chunk assignment

        return chnk


class ChunkInline(admin.StackedInline):
    model = Chunk
    form=CreateChunkForm
    extra=0

class LoadAdmin(admin.ModelAdmin):
    list_display = [
        'uid',
        'offset'
    ]
    list_select_related = []
    list_filter = []
    actions = []
    inlines = (LoadConfigurationInline, ChunkInline,)
