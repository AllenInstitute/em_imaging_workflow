from at_em_imaging_workflow.models import (
    Chunk,
    ChunkAssignment,
    EMMontageSet,
    Load,
    ReferenceSet
)
from workflow_engine.models import (
    Job,
    RunState,
    WorkflowNode
)
import pandas as pd
from django_pandas.io import read_frame
import itertools as it


class FasterJobGrid(object):
    RUN_STATE_LETTERS = {
        "PENDING": "p",
        "QUEUED": 'q',
        "RUNNING": 'r',
        "FINISHED_EXECUTION": 'n',
        "SUCCESS": 's',
        "FAILED": 'f',
        "FAILED_EXECUTION": 'x',
        "PROCESS_KILLED": 'k',
    }
    SERIALIZE_COLUMNS = [
        'z_index',
        'true_z',
        'object_state_id',
        'workflow_node',
        'letter_code',
        'job_id',
        'enqueued_object_type',
        'enqueued_object_id',
        'start',
        'end'
    ]

    def __init__(self, tape_uid, z_range, order):
        self.tape_uid = tape_uid
        self.z_range = z_range
        self.order = order
        self.job_df = None
        self.node_id_order = None
        self.run_state_df = None
        self.z_mapping_df = None
        self.montage_section_z_df = None
        self.reference_section_z_df = None
        self.load_section_z_df = None
        self.chunk_section_z_df = None
        self.grid_df = None
        self.workflow_node_df = None
        self.model_classes = [
            EMMontageSet,
            Chunk,
            ChunkAssignment,
            Load,
            ReferenceSet
        ]
        self.model_types = [
            "chunk",
            "chunkassignment",
            "emmontageset",
            "load",
            "referenceset"
        ]

    def query_node_id_order(self):
        self.node_id_order = [
            n.id for n in it.chain.from_iterable(WorkflowNode.objects.filter(
                workflow__name__in=['em_2d_montage', 'rough_align_em_2d'],
                job_queue__name=job_queue_name
            ) for job_queue_name in self.order)
        ]

        return self.node_id_order
        
    def query_job_df(self):
        self.job_df = read_frame(
            Job.objects.filter(
                enqueued_object_type__model__in=self.model_types,
            ).values(
                'id',
                'enqueued_object_type__model',
                'enqueued_object_id',
                'workflow_node__id',
                'run_state__id',
                'start_run_time',
                'end_run_time'
            ).order_by(# don't have to sort in the database if we do it in pandas
                'enqueued_object_id',
                'workflow_node_id',  # sort by order later
                'run_state_id'
            )
        )
        self.job_df.columns = [
            'job_id', 'enqueued_object_type', 'enqueued_object_id', 'workflow_node', 'run_state_id', 'start', 'end'
        ]

        return self.job_df

    def build_run_state_df(self):
        run_state_letters_df = pd.DataFrame.from_dict(
            FasterJobGrid.RUN_STATE_LETTERS,
            orient='index'
        )
        run_state_letters_df.reset_index(level=0, inplace=True)
        run_state_letters_df.columns = ['run_state', 'letter_code']

        run_state_names_df = read_frame(
            RunState.objects.values(
                'id',
                'name'
            )
        )
        run_state_names_df.columns = ['run_state_id', "run_state"]

        self.run_state_df = run_state_names_df.merge(
            run_state_letters_df,
            on='run_state'
        )

        return self.run_state_df

    def query_offset_z_range(self):
        load_object = Load.objects.get(uid=self.tape_uid)
        
        z_range = (
            self.z_range[0] + load_object.offset,
            self.z_range[1] + load_object.offset
        )

        return z_range

    def query_z_mapping_df(self):
        load_object = Load.objects.get(uid=self.tape_uid)
        z_range = self.query_offset_z_range()

        try:
            z_mapping_json = {
                int(z): true_z for z, true_z in load_object.get_z_mapping().items()
            }
        except:
            z_mapping_json = {
                z: z for z in range(z_range[0], z_range[1] + 1)
            }

        self.z_mapping_df = pd.DataFrame.from_dict(
            z_mapping_json,
            orient='index'
        )

        self.z_mapping_df.reset_index(level=0, inplace=True)
        self.z_mapping_df.columns = ['z_index', 'true_z']

        return self.z_mapping_df

    def query_montage_section_z_df(self):
        z_range = self.query_offset_z_range()

        self.montage_section_z_df = read_frame(
            EMMontageSet.objects.values(
                'id',
                'section__z_index',
                'object_state'
            ).filter(
                section__z_index__gte=z_range[0],
                section__z_index__lte=z_range[1] 
            ).order_by(
                'section__z_index'
            )
        )
        self.montage_section_z_df.columns = ['enqueued_object_id', 'z_index', "object_state"]
        self.montage_section_z_df['enqueued_object_type'] = 'emmontageset'

        return self.montage_section_z_df

    def query_reference_section_z_df(self):
        z_range = self.query_offset_z_range()

        self.reference_section_z_df = read_frame(
            EMMontageSet.objects.values(
                'reference_set__id',
                'section__z_index',
                'object_state'
            ).filter(
                section__z_index__gte=z_range[0],
                section__z_index__lte=z_range[1] 
            ).order_by(
                'section__z_index'
            )
        )
        self.reference_section_z_df.columns = ['enqueued_object_id', 'z_index', "object_state"]
        self.reference_section_z_df['enqueued_object_type'] = 'referenceset'

        return self.reference_section_z_df

    def query_load_section_z_df(self):
        z_range = self.query_offset_z_range()

        self.load_section_z_df = read_frame(
            EMMontageSet.objects.values(
                'sample_holder__load__id',
                'section__z_index',
                'sample_holder__load__object_state'
            ).filter(
                section__z_index__gte=z_range[0],
                section__z_index__lte=z_range[1] 
            ).order_by(
                'section__z_index'
            )
        )
        self.load_section_z_df.columns = ['enqueued_object_id', 'z_index', "object_state"]
        self.load_section_z_df['enqueued_object_type'] = 'load'

        return self.load_section_z_df

    def query_chunk_section_z_df(self):
        z_range = self.query_offset_z_range()

        self.chunk_section_z_df = read_frame(
            EMMontageSet.objects.values(
                'section__chunks__id',
                'section__z_index',
                'section__chunks__object_state'
            ).filter(
                section__z_index__gte=z_range[0],
                section__z_index__lte=z_range[1] 
            ).order_by(
                'section__z_index'
            )
        )
        self.chunk_section_z_df.columns = ['enqueued_object_id', 'z_index', "object_state"]
        self.chunk_section_z_df['enqueued_object_type'] = 'chunk'

        return self.chunk_section_z_df

    def query_object_state_df(self):
        self.object_state_df = pd.concat(
            [
                read_frame(
                    clz.objects.values(
                        'object_state',
                    ).distinct()
                )
                for clz in self.model_classes
            ]
        ).drop_duplicates().reset_index(drop=True)
        self.object_state_df.reset_index(level=0, inplace=True)
        self.object_state_df.columns = (['object_state_id', 'object_state'])

        return self.object_state_df

    def generate_grid_df(self):
        self.grid_df = self.z_mapping_df.merge(
            pd.concat(
                [
                    self.reference_section_z_df,
                    self.montage_section_z_df,
                    self.load_section_z_df,
                    self.chunk_section_z_df
                ]
            ),
            on='z_index',
            how='left'
        ).merge(
            self.job_df,
            on=['enqueued_object_type', 'enqueued_object_id'],
            how='left'
        ).merge(
            self.object_state_df,
            on='object_state',
            how='left'
        )

        return self.grid_df

    def annotate_job_df(self):
        self.annotated_job_df = self.grid_df.merge(
           self.run_state_df,
           on='run_state_id',
           how='left'
        )

        return self.annotated_job_df

    def query_workflow_node_df(self):
        self.workflow_node_df = read_frame(
            WorkflowNode.objects.values(
                'id',
                'job_queue__name'
            ).filter(
                id__in=self.node_id_order,
            )
        )
        self.workflow_node_df.columns = [
            'workflow_node_id', 'workflow_node'
        ]

        return self.workflow_node_df

    def get_dict(self):
        node_id_order = self.query_node_id_order()
        self.query_job_df()
        run_state_df = self.build_run_state_df()
        self.query_z_mapping_df()
        self.query_montage_section_z_df()
        self.query_reference_section_z_df()
        self.query_load_section_z_df()
        self.query_chunk_section_z_df()
        object_state_df = self.query_object_state_df()
        self.generate_grid_df()
        annotated_job_df = self.annotate_job_df()
        workflow_node_df = self.query_workflow_node_df()

        serial_df = annotated_job_df[
            FasterJobGrid.SERIALIZE_COLUMNS
        ].fillna(value=-1)
        z_range = self.query_offset_z_range()
        serial_df = serial_df[
            (serial_df.z_index >= z_range[0]) & 
            (serial_df.z_index <= z_range[1])
        ]
        serial_json = serial_df.to_dict(orient='split')
        del serial_json['index']

        payload = serial_json
        payload['run_states_by_id'] = run_state_df.set_index('run_state_id').fillna(value=-1).to_dict(orient='index')
        payload['run_states_by_letter'] = run_state_df.set_index('letter_code').fillna(value=-1).to_dict(orient='index')
        payload.update(workflow_node_df.set_index('workflow_node_id').fillna(value=-1).to_dict())
        payload['node_order'] = node_id_order
        payload.update(object_state_df.set_index('object_state_id').to_dict())

        return payload
