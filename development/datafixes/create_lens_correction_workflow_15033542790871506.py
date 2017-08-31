#!/usr/bin/python
from django.db import transaction
from workflow_engine.models import *
from development.models import *

@transaction.atomic
def populate_database():
	pbs_queue = 'mindscope'
	batch_size = 20
	max_retries = 1
	enqueued_object_class = 'ReferenceSet'

	#generate_lens_correction_transform
	generate_lens_correction_transform_executable = Executable(name='generate_lens_correction_transform', description='', executable_path='/allen/programs/celltypes/workgroups/array_tomography/blue_sky/run_python/run_python.sh /allen/programs/celltypes/workgroups/array_tomography/blue_sky/render-modules/rendermodules/lens_correction/apply_lens_correction.py', pbs_queue=pbs_queue, pbs_processor='vmem=16g', pbs_walltime='walltime=5:00:00')
	generate_lens_correction_transform_executable.save()

	#apply_to_previously_uploaded_montage_sets_
	apply_to_previously_uploaded_montage_sets_executable = Executable(name='apply_to_previously_uploaded_montage_sets', description='', executable_path='/allen/programs/celltypes/workgroups/array_tomography/blue_sky/run_python/run_python.sh TODO', pbs_queue=pbs_queue, pbs_processor='vmem=16g', pbs_walltime='walltime=5:00:00')
	apply_to_previously_uploaded_montage_sets_executable.save()


	##############################
	#generate_lens_correction_transform
	generate_lens_correction_transform_queue = JobQueue(name='generate_lens_correction_transform_queue', job_strategy_class='GenerateLensCorrectionTransformStrategy', enqueued_object_class=enqueued_object_class, executable=generate_lens_correction_transform_executable)
	generate_lens_correction_transform_queue.save()

	#apply_to_previously_uploaded_montage_sets_
	apply_to_previously_uploaded_montage_sets_queue = JobQueue(name='apply_to_previously_uploaded_montage_sets_queue', job_strategy_class='ApplyToPreviouslyUploadedMontageSetsStrategy', enqueued_object_class=enqueued_object_class, executable=apply_to_previously_uploaded_montage_sets_executable)
	apply_to_previously_uploaded_montage_sets_queue.save()

	##############################

	workflow = Workflow(name='Lens Correction Workflow', description='', use_pbs=False)
	workflow.save()

	###############################

	generate_lens_correction_transform_node = WorkflowNode(job_queue=generate_lens_correction_transform_queue, is_head=True, workflow=workflow, batch_size=batch_size, max_retries=max_retries)
	generate_lens_correction_transform_node.save()

	apply_to_previously_uploaded_montage_sets_node = WorkflowNode(job_queue=apply_to_previously_uploaded_montage_sets_queue, parent=generate_lens_correction_transform_node, workflow=workflow, batch_size=batch_size, max_retries=max_retries)
	apply_to_previously_uploaded_montage_sets_node.save()
	
populate_database()