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
        enqueued_ids = list(df.enqueued_object_id)

        msets = read_frame(
            EMMontageSet.objects.select_related(
                'section').filter(
                    id__in=enqueued_ids).values_list(
                'id', 'section__z_index'))
        df = df.merge(
            msets, left_on='enqueued_object_id', right_on='id', how='left')

        wnodes = read_frame(WorkflowNode.objects.all())

        df = df.merge(
            wnodes, left_on='workflow_node', right_on='id', how='left')

        run_states = read_frame(RunState.objects.all())

        df = df.merge(
            run_states, left_on='run_state', right_on='id', how='left')

        df = df.sort_values(
            by=['end_run_time'], axis='rows',
            ascending=True, na_position='first')

        return pd.pivot_table(df,
        values='name',
        index=['section'],
        columns=['job_queue'],
        aggfunc='last')

