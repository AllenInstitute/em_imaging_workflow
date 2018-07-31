from rest_pandas import PandasView
from rest_pandas.renderers import PandasCSVRenderer
from rest_pandas.renderers import PandasJSONRenderer
from workflow_engine.models.job import Job
from development.models.e_m_montage_set import EMMontageSet
from workflow_engine.models.workflow_node import WorkflowNode
from development.models.chunk import Chunk
from workflow_engine.models.run_state import RunState
from at_em_imaging_workflow.serializers.progress_serializer \
    import ProgressSerializer
import pandas as pd
from django_pandas.io import read_frame


class ProgressView(PandasView):
    queryset = Job.objects.filter(
        workflow_node__workflow__name='em_2d_montage')
    serializer_class = ProgressSerializer
    renderer_classes = [PandasCSVRenderer, PandasJSONRenderer]

    def filter_queryset(self, qs):
        clz = 'development.models.e_m_montage_set.EMMontageSet'

        return qs.filter(
        workflow_node__job_queue__enqueued_object_class=clz,
        archived=False)

    def transform_dataframe(self, df):
        df.loc[:,'job_id'] = df.index
        enqueued_ids = list(df.enqueued_object_id)

        mset_query = EMMontageSet.objects.prefetch_related(
            'section__chunks').select_related(
                'section').filter(
                    id__in=enqueued_ids).order_by('id') # .values_list(
                        #'id',
                        #'section__z_index') 

        msets = read_frame(mset_query)
        msets.loc[:,'z_index'] = msets.section.map(int)
        msets = msets.sort_values(['z_index'])
        msets.loc[:,'em_montage_set_id'] = msets['id']

#         chunks_list = [s.section.chunks.all() for s in mset_query]
#         msets.loc[:, 'chunk1'] = [
#             str(c[0]) if len(c) > 0 else '-' for c in chunks_list]
#         msets.loc[:, 'chunk2'] = [
#             str(c[1]) if len(c) > 1 else '-' for c in chunks_list]
        
        msets.loc[:, 'chunks'] = list(
            map('/'.join,
                list([
                    str(d.computed_index)
                    for d in c.section.chunks.order_by('computed_index').all()]
                    for c in mset_query.order_by('section__z_index'))))

        df = df.merge(
            msets,
            left_on='enqueued_object_id',
            right_on='em_montage_set_id', how='left')

        wnodes = read_frame(WorkflowNode.objects.all())

        df = df.merge(
            wnodes, left_on='workflow_node', right_on='id', how='left')

        run_states = read_frame(RunState.objects.all())

        df = df.merge(
            run_states,
            left_on='run_state',
            right_on='id',
            how='left')

        df = df.sort_values(
            by=['z_index', 'end_run_time'], axis='rows',
            ascending=[True, True], na_position='first')

        df.loc[:,'job_and_state'] = \
            df['job_id'].apply(str) + '/' + \
            df['name'] + '/' + df['em_montage_set_id'].apply(str)

        pt = pd.pivot_table(df,
            values='job_and_state',
            index='z_index',
            columns=['job_queue'],
            aggfunc='last')

        min_z = pt.index.min()
        max_z = pt.index.max()

        extra_df = df.sort_values(
            'end_run_time').groupby(
                'z_index').agg(
                    lambda x: x.iloc[-1]).loc[
                        :,
                        ['workflow_state',
                         'chunks']]

        pt = pt.join(
            extra_df,
            how='left')

        pt.loc[-1,:] = pt.count()

        show_blanks = False

        if show_blanks:
            index_by_one = pd.Index(
                range(int(min_z), int(max_z) + 1),
                name='z_index')
            pt = pt.reindex(index_by_one).reset_index()
 
        return pt
