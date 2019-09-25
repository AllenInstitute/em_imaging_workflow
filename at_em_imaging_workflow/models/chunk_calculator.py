from at_em_imaging_workflow.models import (
    Chunk,
    ChunkAssignment,
    RenderedVolume,
    Section
)

class ChunkCalculator(object):
    @classmethod
    def calculate_chunk_sizes_mod_16(cls, load, overlap=100):
        mapping = {
            int(k): v
            for k,v in load.get_z_mapping().items()
        }
        reverse_mapping = { v: k for k,v in mapping.items()}
        reverse_mapping_mod_16 = {
            v: k for v,k in reverse_mapping.items() if v % 16 == 0
        }

        return reverse_mapping_mod_16

    @classmethod
    def create_chunk(cls,
        load_object, computed_index, z_min, z_max, volume=None):

        if volume is None:
            volume = RenderedVolume.objects.first()
    
        chnk,_ = Chunk.objects.get_or_create(
            computed_index=computed_index,
            defaults = {
                'size': 0,
                'object_state': Chunk.STATE.CHUNK_INCOMPLETE,
                'rendered_volume': volume,
                'preceding_chunk': None,
                'following_chunk': None
            }
        )

        load_object.chunk_set.add(chnk)

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
            z_index__lte=z_max
        )

        for s in sections:
            ChunkAssignment.objects.get_or_create(
                section=s,
                chunk=chnk
            )

        return chnk
