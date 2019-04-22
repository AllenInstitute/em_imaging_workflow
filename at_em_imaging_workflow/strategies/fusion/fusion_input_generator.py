from at_em_imaging_workflow.two_d_stack_name_manager import TwoDStackNameManager
import simplejson as json


class FusionInputGenerator(object):
    ROUGH_ALIGNMENT='rough_align_em_2d'
    REGISTER_ADJACENT='Register Adjacent Stack'
    ROUGH_SOLVER='Rough Align Python Solver 2'
    DEFAULT_STACK_NAME='FUSEDOUTSTACK'
    STACK_30_31_33='FUSEDOUTSTACK_Chunk_30_31_33'
    
    def __init__(self, chnk):
        self.chunk = chnk # EnqueuedObject(chnk)

    @classmethod
    def get_job(cls, chnk, queue_name):
        return chnk.jobs().get(
            workflow_node__workflow__name=(
                cls.ROUGH_ALIGNMENT
            ),
            workflow_node__job_queue__name=(
                queue_name
            )
        )

    @classmethod
    def get_output_file(cls, chnk, queue_name):
        the_job = cls.get_job(chnk, queue_name)
        the_strategy = the_job.get_strategy()
        the_task = the_job.tasks().get()

        output_file = the_strategy.get_output_file(
            the_task
        )

        return output_file

    @classmethod
    def get_output_json(cls, chnk, queue_name):
        with open(cls.get_output_file(chnk, queue_name)) as f:
            output_json = json.load(f)

        return output_json

    def get_fusion_transform(self, chnk=None):
        if chnk is None:
            chnk = self.chunk

        transform_dict = None

        try:
            transform_dict = chnk.configurations.get(
                configuration_type='fusion_transform' 
            ).json_object
        except:
            pass

        return transform_dict

    def fused_stack_name(self):
        stack_name = FusionInputGenerator.DEFAULT_STACK_NAME

        return stack_name

    def chunk_chain(self):
        c = self.chunk # self.chunk.eo
        chunks = [c] # [EnqueuedObject(c)]

        while c:
            c = c.preceding_chunk

            if c:
                chunks.insert(0, c) # EnqueuedObject(c))

        return chunks

    def stacks_json(self):
        top_stacks = []
        stacks = top_stacks
        fuse_stack = top_stacks

        for c in self.chunk_chain():
            #print(c.eo)
            oj = self.get_fusion_transform(c)

            if oj is None:
                try:
                    oj = self.get_output_json(
                        c, FusionInputGenerator.REGISTER_ADJACENT)
                    del oj['stack_b']
                    del oj['stack_a']
                except:
                    oj = { "OOPS": "ERROR"}

            # TODO: verify we don't want to use the previous output
            #solve_oj = self.get_output_json(
            #    c, FusionInputGenerator.ROUGH_SOLVER
            #)

            solve_rough_align_affine_stacks = \
                TwoDStackNameManager.solve_rough_align_python_stacks(
                    c, TwoDStackNameManager.TRANSFORM.AFFINE
                )
            oj['stack'] = solve_rough_align_affine_stacks['output_stack']
            oj['fuse_stack'] = False
            fuse_stack = oj
            oj['children'] = []

            stacks.append(oj)
            stacks = oj['children']

        fuse_stack['fuse_stack'] = True
        return { "stacks": top_stacks }

    def status(self):
        print(self.chunk.eo.computed_index)
