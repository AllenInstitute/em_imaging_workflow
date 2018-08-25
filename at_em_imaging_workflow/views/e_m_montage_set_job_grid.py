from workflow_engine.views.job_grid import JobGrid
from development.models.e_m_montage_set import EMMontageSet
from django_pandas.io import read_frame


class EMMontageSetJobGrid(JobGrid):
    def index_field(self):
        return 'z_index'

    def extra_columns(self):
        return ['workflow_state', 'chunks']

    def query_enqueued_objects(self):
        self.enqueued_objects = EMMontageSet.objects.prefetch_related(
            'section__chunks').select_related(
                'section').order_by('section__z_index')
        self.enqueued_object_df = read_frame(
            self.enqueued_objects, index_col='id')
        self.enqueued_object_df = self.enqueued_object_df[['workflow_state', 'section']]
        self.enqueued_object_df = self.enqueued_object_df.dropna(subset=['section'])
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
            (self.sorted_nodes_df.enqueued_object_type=='em montage set') &
            (self.sorted_nodes_df.workflow != 'matlab_montage_solver')]

