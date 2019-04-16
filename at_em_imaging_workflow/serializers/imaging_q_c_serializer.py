from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.fields import DateTimeField
from at_em_imaging_workflow.models import EMMontageSet


class ImagingQCSerializer(ModelSerializer):
    acquisition_date = DateTimeField(format='iso-8601')
    #sample_holder = PrimaryKeyRelatedField(
    #        many=False,
    #        read_only=True)

    class Meta:
        model = EMMontageSet
        fields = ('id', 'object_state', 'sample_holder', 'section')
