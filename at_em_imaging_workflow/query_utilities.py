import pandas as pd
from django_pandas.io import read_frame
from workflow_engine.models.job import Job
from django.contrib.contenttypes.models import ContentType


class QueryUtilities(object):

    @classmethod
    def make_job_object_df(model_class, **kwargs):
        enqueued_objects = model_class.objects.filter(**kwargs)
        enqueued_objects_df = read_frame(enqueued_objects, index_col='id')
    
        js = Job.objects.filter(
            enqueued_object_type=ContentType.objects.get_for_model(model_class),
            archived=False)
        js_df = read_frame(js)
    
        job_df = js_df.merge(
            enqueued_objects_df,
            left_on='enqueued_object_id',
            right_index=True)
    
        return job_df