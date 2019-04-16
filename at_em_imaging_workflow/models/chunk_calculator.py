class ChunkCalculator(object):
    @classmethod
    def calculate_chunk_sizes_mod_16(cls, load, overlap=100):
        mapping = {
            int(k): v
            for k,v in load.configurations.get(
                configuration_type='z_mapping'
            ).json_object.items()
        }
        reverse_mapping = { v: k for k,v in mapping.items()}
        reverse_mapping_mod_16 = {
            v: k for v,k in reverse_mapping if v % 16 == 0
        }

        return reverse_mapping_mod_16
