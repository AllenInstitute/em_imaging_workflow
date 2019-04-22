from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from at_em_imaging_workflow.models import (
    ChunkCalculator,
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

    return ChunkCalculator.create_chunk(
        load_object, computed_index, z_min, z_max, volume)

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
    success_url = reverse_lazy('admin:at_em_imaging_workflow_chunk_changelist')

    def form_valid(self, form):
        form.do_create()
        return super().form_valid(form)
