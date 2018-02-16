from workflow_engine.models.well_known_file import WellKnownFile
from workflow_engine.models.file_record import FileRecord
from django.contrib.contenttypes.models import ContentType
from workflow_engine.workflow_controller import WorkflowController
from workflow_engine.strategies.execution_strategy \
    import ExecutionStrategy
import logging


class ChmodStrategy(ExecutionStrategy):
    _log = logging.getLogger(
        'development.strategies.chmod_strategy')
    CHMOD_DIR_PENDING = 'chmod_dir_pending'
    CHMOD_FILE_PENDING = 'chmod_file_pending'
    CHMOD_DIR_PROCESSING = 'chmod_dir_processing'
    CHMOD_FILE_PROCESSING = 'chmod_file_processing'
    CHMOD_DIR_COMPLETE = 'chmod_dir_processing'
    CHMOD_FILE_COMPLETE = 'chmod_file_processing'

    def get_input(self, em_mset, storage_directory, task):
        dir_wkfs = WellKnownFile.objects.filter(
            attachable_id=em_mset.id,
            well_known_file_type=ChmodStrategy.CHMOD_DIR_PENDING)

        dirs = []
        for w in dir_wkfs:
            dirs.append(
                w.get_most_recent_file_record().get_full_name())
            w.well_known_file_type = ChmodStrategy.CHMOD_DIR_PROCESSING
            w.save()

        file_wkfs = WellKnownFile.objects.filter(
            attachable_id=em_mset.id,
            well_known_file_type=ChmodStrategy.CHMOD_FILE_PENDING)

        files = []
        for w in file_wkfs:
            files.append(
                w.get_most_recent_file_record().get_full_name())
            w.well_known_file_type = ChmodStrategy.CHMOD_FILE_PROCESSING
            w.save()

        inp = {
            'dirs': dirs,
            'files': files
        }

        return inp

    def on_finishing(self, em_mset, results, task):
        processing = [
            ChmodStrategy.CHMOD_DIR_PROCESSING,
            ChmodStrategy.CHMOD_FILE_PROCESSING]

        wkfs = ChmodStrategy.find_chmod_files(
            em_mset, processing)

        for w in wkfs:
            if w.well_known_file_type==ChmodStrategy.CHMOD_DIR_PROCESSING:
                w.well_known_file_type=ChmodStrategy.CHMOD_DIR_COMPLETE
            elif w.well_known_file_type==ChmodStrategy.CHMOD_FILE_PROCESSING:
                w.well_known_file_type=ChmodStrategy.CHMOD_FILE_COMPLETE
            w.save()


    @classmethod
    def find_chmod_files(
        cls, attachable, type_list):

        t = ContentType.objects.get_for_model(
            attachable.__class__)
    
        wkfs = WellKnownFile.objects.filter(
            attachable_type=t,
            attachable_id=attachable.id,
            well_known_file_type__in=type_list)

        return wkfs

    @classmethod
    def add_chmod_file(
        cls, attachable_object, base_dir):
        wkf = WellKnownFile.objects.create(
            content_object=attachable_object,
            well_known_file_type=ChmodStrategy.CHMOD_FILE_PENDING)
        fr = FileRecord.objects.create(
            storage_directory=base_dir,
            filename="",
            well_known_file=wkf)
        fr.save()
        wkf.save()

        return wkf

    @classmethod
    def add_chmod_dir(
        cls, attachable_object, base_dir):
        wkf = WellKnownFile.objects.create(
            content_object=attachable_object,
            well_known_file_type=ChmodStrategy.CHMOD_DIR_PENDING)
        fr = FileRecord.objects.create(
            storage_directory=base_dir,
            filename="",
            well_known_file=wkf)
        fr.save()
        wkf.save()

        return wkf

    @classmethod
    def enqueue_montage(cls, em_mset):
        WorkflowController.start_workflow(
            'em_2d_montage',
            em_mset,
            start_node_name='Chmod Montage')

    @classmethod
    def enqueue_reference(cls, ref_set):
        WorkflowController.start_workflow(
            'em_2d_montage',
            ref_set,
            start_node_name='Chmod Reference')