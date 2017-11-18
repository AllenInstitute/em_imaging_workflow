import os
from development.models import *
from rendermodules.ingest.schemas import \
    example, EMMontageSetIngestSchema

class IngestCallbacks(object):
    @classmethod
    def cb(cls, message):
        IngestCallbacks.create_reference_set(messgage)
 
    @classmethod
    def create_enqueued_object(cls, message):
        workflow = 'lens_correction_new' 
        enqueued_object = IngestCallbacks.create_reference_set(message)
 
        return workflow, enqueued_object

    @classmethod
    def create_reference_set(cls, message):
        message_camera = message['acquisition_data']['camera']
        camera, _ = \
            Camera.objects.update_or_create(
                uid=message_camera['camera_id'],
                defaults={
                    'height': message_camera['height'],
                    'width': message_camera['width'],
                    'model': message_camera['model']})

        microscope_type, _ = \
            MicroscopeType.objects.update_or_create(
                name=message['acquisition_data']['microscope'])

        microscope, _ = \
            Microscope.objects.update_or_create(
                uid="DEADBEEF",
                defaults={
                    'microscope_type': microscope_type
                })

        storage_directory, metafile = \
            os.path.split(message['acquisition_data']['metafile'])

        reference_set, _ = ReferenceSet.objects.update_or_create(
                uid=message['reference_set_id'],
                defaults={
                    'storage_directory': storage_directory,
                    'workflow_state': 'Pending',
                    'camera': camera,
                    'microscope': microscope,
                    # 'project_path': '/example_data' # deprecated
                })

        return reference_set # TODO: return reference_set id to ingest client
