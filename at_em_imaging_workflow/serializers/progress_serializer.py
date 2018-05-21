from workflow_engine.models.job import Job
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import DateTimeField, TimeField


class ProgressSerializer(ModelSerializer):
    start_run_time = DateTimeField(format='iso-8601')
    end_run_time = DateTimeField(format='iso-8601')

    class Meta:
        model = Job
        fields = [
	    'id', 'start_run_time', 'end_run_time', 'enqueued_object_id',
	    'run_state', 'workflow_node' ]
