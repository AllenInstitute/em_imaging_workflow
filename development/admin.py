from django.contrib import admin
from development.models.a_t_montage_set import ATMontageSet
from development.models.camera import Camera
from development.models.chunk import Chunk
from development.models.e_m_montage_set import EMMontageSet
from development.models.load import Load
from development.models.microscope import Microscope
from development.models.microscope_type import MicroscopeType
from development.models.montage_set import MontageSet
from development.models.registration_series import RegistrationSeries
from development.models.reference_set import ReferenceSet
from development.models.rendered_volume import RenderedVolume
from development.models.sample_holder import SampleHolder
from development.models.section import Section
from development.models.stain import Stain
from development.models.specimen import Specimen
from development.models.study import Study
from development.models.tile_image_set import TileImageSet
from at_em_imaging_workflow.admin.e_m_montage_set_admin \
    import EMMontageSetAdmin


# Register your models here.
admin.site.register(ATMontageSet)
admin.site.register(Camera)
admin.site.register(Chunk)
admin.site.register(EMMontageSet, EMMontageSetAdmin)
admin.site.register(Load)
admin.site.register(Microscope)
admin.site.register(MicroscopeType)
admin.site.register(MontageSet)
admin.site.register(RegistrationSeries)
admin.site.register(ReferenceSet)
admin.site.register(RenderedVolume)
admin.site.register(SampleHolder)
admin.site.register(Section)
admin.site.register(Stain)
admin.site.register(Specimen)
admin.site.register(Study)
admin.site.register(TileImageSet)
admin.site.disable_action('delete_selected')