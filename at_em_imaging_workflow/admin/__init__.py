from django.contrib import admin
from ..models import (
    Camera,
    Chunk,
    ChunkAssignment,
    EMMontageSet,
    Load,
    Microscope,
    MicroscopeType,
    MontageSet,
    RegistrationSeries,
    ReferenceSet,
    RenderedVolume,
    SampleHolder,
    Section,
    Stain,
    Specimen,
    Study,
    TileImageSet,
)
from .e_m_montage_set_admin import EMMontageSetAdmin
from .reference_set_admin import ReferenceSetAdmin
from .chunk_admin import ChunkAdmin
from .rendered_volume_admin import RenderedVolumeAdmin
from .section_admin import SectionAdmin
from .sample_holder_admin import SampleHolderAdmin
from .load_admin import LoadAdmin


# Register your models here.
for m in (
    Camera,
    ChunkAssignment,
    Microscope,
    MicroscopeType,
    MontageSet,
    RegistrationSeries,
    Stain,
    Specimen,
    Study,
    TileImageSet,
):
    admin.site.register(m)
    
admin.site.register(Chunk, ChunkAdmin)
admin.site.register(EMMontageSet, EMMontageSetAdmin)
admin.site.register(Load, LoadAdmin)
admin.site.register(ReferenceSet, ReferenceSetAdmin)
admin.site.register(RenderedVolume, RenderedVolumeAdmin)
admin.site.register(SampleHolder, SampleHolderAdmin)
admin.site.register(Section, SectionAdmin)
# admin.site.disable_action('delete_selected')
