from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.fields import DateTimeField
from development.models.e_m_montage_set import EMMontageSet


class ImagingQCSerializer(ModelSerializer):
    acquisition_date = DateTimeField(format='iso-8601')
    #sample_holder = PrimaryKeyRelatedField(
    #        many=False,
    #        read_only=True)

    class Meta:
        model = EMMontageSet
        fields = ('id', 'object_state', 'sample_holder', 'section')
