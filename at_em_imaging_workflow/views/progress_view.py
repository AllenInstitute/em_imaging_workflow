from rest_pandas import PandasView
from rest_pandas.renderers import PandasCSVRenderer
from rest_pandas.renderers import PandasJSONRenderer
from workflow_engine.models.job import Job
from development.models.e_m_montage_set import EMMontageSet
from workflow_engine.models.workflow_node import WorkflowNode
from workflow_engine.models.run_state import RunState
from at_em_imaging_workflow.serializers.progress_serializer \
    import ProgressSerializer
import pandas as pd
from django_pandas.io import read_frame


class ProgressView(PandasView):
    queryset = Job.objects.all()
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

        msets = read_frame(
            EMMontageSet.objects.select_related(
                'section').filter(
                    id__in=enqueued_ids).values_list(
                'id', 'section__z_index'))
        msets.loc[:,'z_index'] = msets.section.map(int)
        msets.loc[:,'em_montage_set_id'] = msets['id']

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
            by=['end_run_time'], axis='rows',
            ascending=True, na_position='first')

        df.loc[:,'job_and_state'] = \
            df['job_id'].apply(str) + '/' + \
            df['name'] + '/' + df['em_montage_set_id'].apply(str)

        pt =  pd.pivot_table(df,
            values='job_and_state',
            index='z_index',
            columns=['job_queue'],
            aggfunc='last')

        pt['z_index'] = pt.index.map(int)
        min_z = pt['z_index'].min()
        max_z = pt['z_index'].max()
        index_by_one = pd.Index(
            range(int(min_z), int(max_z) + 1),
            name='z_index')
        pt = pt.set_index('z_index').reindex(index_by_one).reset_index()

        return pt
