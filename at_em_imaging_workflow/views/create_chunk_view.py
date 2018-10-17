from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from development.models import (
    Chunk,
    ChunkAssignment,
    Section,
    RenderedVolume,
    Load
)
from django.forms import (
    Form,
    IntegerField,
    CharField
)


def create_chunk_handler(
    load_object, computed_index, z_min, z_max, volume=None):
    if volume is None:
        volume = RenderedVolume.objects.first()

    chnk,_ = Chunk.objects.get_or_create(
        computed_index=computed_index,
        defaults = {
            'size': 0,
            'chunk_state': Chunk.STATE.CHUNK_INCOMPLETE,
            'rendered_volume': volume,
            'preceding_chunk': None,
            'following_chunk': None
        }
    )

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

    z_mapping,_ = chnk.configurations.update_or_create(
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


class CreateChunkForm(Form):
    load_name = CharField(max_length=255)
    computed_index = IntegerField()
    z_min = IntegerField()
    z_max = IntegerField()
    volume_name = CharField(max_length=255)

    def do_create(self):
        return create_chunk_handler(
            load_object=Load.objects.get(
                uid=self.cleaned_data['load_name']),
            computed_index=self.cleaned_data['computed_index'],
            z_min=self.cleaned_data['z_min'],
            z_max=self.cleaned_data['z_max'],
            volume=RenderedVolume.objects.get(
                specimen__uid=self.cleaned_data['volume_name']))


class CreateChunkView(FormView):
    template_name = 'create_chunk.html'
    form_class = CreateChunkForm
    success_url = reverse_lazy('admin:development_chunk_changelist')

    def form_valid(self, form):
        form.do_create()
        return super().form_valid(form)
