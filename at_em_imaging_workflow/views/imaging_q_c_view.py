from rest_pandas import PandasView
from development.models.e_m_montage_set import EMMontageSet
from at_em_imaging_workflow.serializers.imaging_q_c_serializer \
    import ImagingQCSerializer


class ImagingQCView(PandasView):
    queryset = EMMontageSet.objects.all()
    serializer_class = ImagingQCSerializer

    def filter_queryset(self, qs):
        state = self.request.GET.get('workflow_state')

        if state is not None:
            qs.filter(workflow_state__in=state.split(','))

        return qs