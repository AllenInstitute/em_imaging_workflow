#!/usr/bin/python
from django.db import transaction
from workflow_engine.models import *
from development.models import *

@transaction.atomic
def populate_database():
    #put your code here
    print('populating database...')

    #TODO set uid correctly
    reference_set = ReferenceSet(uid='0', project_path='/allen/programs/celltypes/workgroups/em-connectomics/data/workflow_test_sqmm/20170829135153_reference/0/')
    reference_set.save()

    job = Workflow.start_workflow('Lens Correction Workflow', reference_set)

populate_database()