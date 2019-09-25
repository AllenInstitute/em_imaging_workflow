from workflow_engine.views.enqueueable_job_grid import EnqueueableJobGrid
from django.contrib.contenttypes.models import ContentType
from at_em_imaging_workflow.models import (
    Chunk,
    ChunkAssignment,
    EMMontageSet,
    Load,
    ReferenceSet
)
from workflow_engine.models import (
    WorkflowNode
)
import pandas as pd
from django_pandas.io import read_frame


class FasterJobGrid(EnqueueableJobGrid):
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
    '''ordered list of columns from the annotated job dataframe to send.
    '''

    def __init__(self, tape_uid, z_range, order=None):
        '''Set up data members to hold partial job grid calculation results.

        Parameters
        ----------
        order: list of strings
            Ordered list of job queue names
        '''
        self.tape_uid = tape_uid
        self.load_object = Load.objects.get(uid=self.tape_uid)
        self.z_range = z_range
        self.z_mapping_df = None
        super(FasterJobGrid, self).__init__(
            self.calculate_offset_z_range(self.load_object, self.z_range)
        )
#         if order is None:
#             self.order = self.get_node_order()
#         else:
#             self.order = order  # TODO: put this in a config object on workflow
#         self.job_df = None
#         self.node_id_order = None
#         self.run_state_df = None
#         self.z_mapping_df = None
#         self.enqueued_object_row_df = None
#         self.grid_df = None
#         self.workflow_node_df = None
#         self.model_classes = self.get_model_classes() 
#         self.model_types = [
#             "chunk",
#             "chunkassignment",
#             "emmontageset",
#             "load",
#             "referenceset"
#         ]

    # TODO: get this from a workflow configuration object or request.
    def get_node_order(self):
        '''Override with a specific list of job queue names.
        These will be used in order as the columns of the job grid.

        Returns
        -------
        list of string
        '''
        return [
            "Ingest Tile Sets",
            "Generate Lens Correction Transform",
            "Generate Render Stack",
            "Generate MIPMaps",
            "Apply MIPMaps",
            "Wait for Lens Correction",
            "Apply Lens Correction",
            "Create Tile Pairs",
            "2D Montage Point Match",
            "2D Montage Python Solver",
            "Detect Defects",
            "Manual QC / High Degree Polynomial or Point Match Regeneration",
            "Load Z Mapping",
            "Chunk Assignment",
            "Wait for Z Mapping",
            "Make Montage Scapes",
            "Remap Zs",
            "Wait for Chunk Assignment",
            "Wait for Complete Chunk",
            "Create Rough Tile Pairs",
            "EM Rough Point Match",
            "Rough Align Python Solver",
            "Rough Align Python Solver 2",
            "Rough Align Manual QC",
            "Apply Rough Alignment",
            "Register Adjacent Stack",
            "Fuse Stacks",
            "Rough Alignment Materialize"
        ]

    # TODO: maybe limit this based on request
    def get_model_classes(self):
        '''Models to be queried for display in the grid.
        Override to provide a specific list of model classes.
        They must implement :class:`workflow_engine.mixins.enqueueable.Enqueueable`
 
        Returns
        -------
        list of Model
            model classes that implement Enqueueable

        Notes
        -----
        By default, immediate subclasses of Enqueueable 
        will be included, but not leaf descendant classes.
        '''
        return [
            EMMontageSet,
            Chunk,
            ChunkAssignment,
            Load,
            ReferenceSet
        ]

    def get_workflow_names(self):
        return ['em_2d_montage', 'rough_align_em_2d']

    def calculate_offset_z_range(self, load_object, z_range):
        '''Apply the microscope Load (tapes) fixed integer offset to the min and max z's.

        Returns
        -------
        tuple of two integers
            min temp z, max temp z

        Notes
        -----
        This should be refactored into the Load object
        '''
        return (
            z_range[0] + load_object.offset,
            z_range[1] + load_object.offset
        )

    def query_row_mapping_df(self):
        '''Get a dataframe relating rows in different coordinates
        Notes
        -----
        z_index column is the temporary z index with generous offsets.
        true_z column is the contiguous z index used for rough alignment.
        If a tape z mapping is not available from an uploaded spreadsheet,
        the relation is calculated using an offset.
        '''
        try:
            z_mapping_json = {
                int(z): true_z for z, true_z in self.load_object.get_z_mapping().items()
            }
        except:
            z_mapping_json = {
                z: z for z in range(self.row_range[0], self.row_range[1] + 1)
            }

        self.z_mapping_df = pd.DataFrame.from_dict(
            z_mapping_json,
            orient='index'
        )

        self.z_mapping_df.reset_index(level=0, inplace=True)
        self.z_mapping_df.columns = ['z_index', 'true_z']

        return self.z_mapping_df

    def query_enqueued_object_row_df(self):
        '''Combine row dataframes across
        EMMontageSet, ReferenceSet, Chunk and Load.
        The sub dataframes all share the montage set z index
        as the row coordinate
        '''
        self.enqueued_object_row_df = pd.concat(
            [
                self.query_montage_section_z_df(),
                self.query_reference_section_z_df(),
                self.query_load_section_z_df(),
                self.query_chunk_section_z_df()
            ]
        ).sort_values('z_index')

        return self.enqueued_object_row_df

    def query_montage_section_z_df(self):
        montage_section_z_df = read_frame(
            EMMontageSet.objects.values(
                'id',
                'section__z_index',
                'object_state'
            ).filter(
                section__z_index__gte=self.row_range[0],
                section__z_index__lte=self.row_range[1] 
            )
        )
        montage_section_z_df.columns = [
            'enqueued_object_id',
            'z_index',              # TODO: change to row
            "object_state"
        ]
        montage_section_z_df['enqueued_object_type'] = 'emmontageset'

        return montage_section_z_df

    def query_reference_section_z_df(self):
        '''Query all load object that are associated with the range of rows

        Notes
        -----
        This filter does not look right, it should be calculated
        through one of the corresponding montage set z_index.
        '''
        reference_section_z_df = read_frame(
            EMMontageSet.objects.values(
                'reference_set__id',
                'section__z_index',
                'object_state'
            ).filter(
                section__z_index__gte=self.row_range[0],
                section__z_index__lte=self.row_range[1] 
            )
        )
        reference_section_z_df.columns = ['enqueued_object_id', 'z_index', "object_state"]
        reference_section_z_df['enqueued_object_type'] = 'referenceset'

        return reference_section_z_df

    def query_load_section_z_df(self):
        load_section_z_df = read_frame(
            EMMontageSet.objects.values(
                'sample_holder__load__id',
                'section__z_index',
                'sample_holder__load__object_state'
            ).filter(
                section__z_index__gte=self.row_range[0],
                section__z_index__lte=self.row_range[1] 
            )
        )
        load_section_z_df.columns = ['enqueued_object_id', 'z_index', "object_state"]
        load_section_z_df['enqueued_object_type'] = 'load'

        return load_section_z_df

    def query_chunk_section_z_df(self):
        chunk_section_z_df = read_frame(
            EMMontageSet.objects.values(
                'section__chunks__id',
                'section__z_index',
                'section__chunks__object_state'
            ).filter(
                section__z_index__gte=self.row_range[0],
                section__z_index__lte=self.row_range[1] 
            )
        )
        chunk_section_z_df.columns = ['enqueued_object_id', 'z_index', "object_state"]
        chunk_section_z_df['enqueued_object_type'] = 'chunk'

        return chunk_section_z_df

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

    def annotate_enqueued_object_row_df(self):
        '''Merge in z_mapping
        '''
        self.annotated_enqueued_object_row_df = self.z_mapping_df.merge(
            self.enqueued_object_row_df,
            on='z_index',    # TODO: change to row_coordinate
            how='left'
        )
        return self.annotated_enqueued_object_row_df

#         self.grid_df = self.z_mapping_df.merge(
#             self.enqueued_object_row_df,
#             on='z_index',    # TODO: change to row_coordinate
#             how='left'
#         ).merge(
#             self.job_df,
#             on=['enqueued_object_type', 'enqueued_object_id'],
#             how='left'
#         ).merge(
#             self.object_state_df,
#             on='object_state',
#             how='left'
#         )
# 
#         return self.grid_df

    def annotate_job_df(self):
        self.annotated_job_df = self.grid_df.merge(
           self.run_state_df,
           on='run_state',
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
        run_state_df = self.build_run_state_df()

        self.query_job_df()
        self.query_row_mapping_df()
        self.query_enqueued_object_row_df()
        object_state_df = self.query_object_state_df()
        self.annotate_enqueued_object_row_df()

        self.generate_grid_df()
        annotated_job_df = self.annotate_job_df()
        workflow_node_df = self.query_workflow_node_df()

        serial_df = annotated_job_df[
            FasterJobGrid.SERIALIZE_COLUMNS
        ].fillna(value=-1)
        serial_df = serial_df[
            (serial_df.z_index >= self.row_range[0]) & 
            (serial_df.z_index <= self.row_range[1])
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
