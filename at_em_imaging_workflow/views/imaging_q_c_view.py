from rest_pandas import PandasView
from at_em_imaging_workflow.models import (
    EMMontageSet,
    SampleHolder,
    Section
)
from at_em_imaging_workflow.serializers.imaging_q_c_serializer import (
    ImagingQCSerializer
)


class ImagingQCView(PandasView):
    queryset = EMMontageSet.objects.prefetch_related(
        'sample_holder',
        'sample_holder__load',
        'section').all()
    serializer_class = ImagingQCSerializer

    def filter_queryset(self, qs):
        state = self.request.GET.get('object_state')

        if state is not None:
            qs.filter(object_state__in=state.split(','))

        return qs

    def transform_dataframe(self, df):
        df.loc[:,'sample_holder_uid'] = df.sample_holder.map(
            lambda x: SampleHolder.objects.get(id=x).uid)
        df.loc[:,'load'] = df.sample_holder.map(
            lambda x: SampleHolder.objects.get(id=x).load.uid)
        df.loc[:,'offset'] = df.sample_holder.map(
            lambda x: SampleHolder.objects.get(id=x).load.offset)
        df.loc[:,'z'] = df.sample_holder.map(
            lambda x: Section.objects.get(id=x).z_index)
        df.loc[:,'name'] = df.id.map(
            lambda x: str(EMMontageSet.objects.get(id=x)))
            
        return df
