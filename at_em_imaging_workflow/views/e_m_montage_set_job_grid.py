from workflow_engine.views.job_grid import JobGrid
from development.models import (
    EMMontageSet,
    ChunkAssignment
)
from django_pandas.io import read_frame


class EMMontageSetJobGrid(JobGrid):
    def sort_columns(self):
        return ['z_index']

    def extra_columns(self):
        return ['z_index', 'object_state', 'chunks']

    def query_enqueued_objects(self):
        self.enqueued_objects = EMMontageSet.objects.prefetch_related(
            'section__chunks').select_related(
                'section').order_by('section__z_index')
        self.enqueued_object_df = read_frame(
            self.enqueued_objects, index_col='id')
        self.enqueued_object_df = self.enqueued_object_df[
            ['object_state', 'section']]
        self.enqueued_object_df = self.enqueued_object_df.dropna(
            subset=['section'])
        self.enqueued_object_df.loc[:,'z_index'] = [
            int(s) for s in list(self.enqueued_object_df['section'])
        ]

        self.enqueued_object_df.loc[:, 'chunks'] = list(
            map('/'.join,
                list([
                    str(d.computed_index)
                    for d in c.section.chunks.order_by('computed_index').all()]
                    for c in self.enqueued_objects)))

    def filter_workflow_nodes(self):
        return self.sorted_nodes_df[
            (self.sorted_nodes_df.job_queue=='Rough Alignment Materialize') |
            ((self.sorted_nodes_df.enqueued_object_type=='em montage set') &
             (self.sorted_nodes_df.workflow != 'matlab_montage_solver'))]

    def chunk_assignment_mapping(self):
        cas = ChunkAssignment.objects.filter(
            id__in=set(self.job_df[
                self.job_df.enqueued_object_type=='chunk assignment'
            ]['enqueued_object_id']))
        ca_df = read_frame(cas, verbose=False)

        msets = EMMontageSet.objects.filter(
            section__id__in=set(
                ca_df['section']))
        msets_df=read_frame(msets, verbose=False)
        #msets_df.loc[:,'z_index'] = msets_df['id'].apply(
        #    lambda x: int(msets.get(id=x).section.z_index))
        mapping_df = msets_df.merge(ca_df, on='section').loc[:,['id_x','id_y']].drop_duplicates()

        materialize_index = self.job_df[
            (self.job_df.enqueued_object_type=='chunk assignment') &
            (self.job_df.enqueued_object_id.notna())
        ].index
        mapped_job_df = self.job_df.loc[
            materialize_index,:
        ].merge(
            mapping_df,
            left_on='enqueued_object_id',
            right_on='id_y',
            how='left')

        mapped_job_df.loc[:,'enqueued_object_id'] = list(mapped_job_df['id_x'].apply(int))

        self.job_df.loc[
            materialize_index,
            'enqueued_object_type'] = 'em montage set'
        self.job_df.loc[
            materialize_index,
            'enqueued_object_id'] = list(mapped_job_df['id_x'])

