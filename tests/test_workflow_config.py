# Allen Institute Software License - This software license is the 2-clause BSD
# license plus a third clause that prohibits redistribution for commercial
# purposes without further permission.
#
# Copyright 2017. Allen Institute. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Redistributions for commercial purposes are not permitted without the
# Allen Institute's written permission.
# For purposes of this license, commercial purposes is the incorporation of the
# Allen Institute's software into anything for which you will charge fees or
# other compensation. Contact terms@alleninstitute.org for commercial licensing
# opportunities.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
import pytest
import os
import importlib
from workflow_engine.workflow_config import WorkflowConfig
from workflow_engine.models import *
from django.db import transaction


@pytest.fixture
def workflow_config():
    return WorkflowConfig


def test_workflow_config(workflow_config):
    assert workflow_config is not None


@transaction.atomic
def test_create_workflow(workflow_config):
    app_package = 'development'

    app_models = importlib.import_module(app_package + '.models')
    app_strategies = importlib.import_module(app_package + '.strategies')

    pbs_queue = 'mindscope'
    pbs_processor='vmem=16g',
    pbs_walltime='walltime=5:00:00'
    wc = workflow_config.from_yaml_file(os.path.join(os.path.dirname(__file__),
                                        'workflows.yml'))

    for workflow_spec in wc:
        workflow_name = workflow_spec.name

        workflow = Workflow(name=workflow_name,
                            description='N/A',
                            use_pbs=False)
        workflow.save()

        executable_number = 1
        queue_number = 1

        mock_executable = \
            Executable(name='%s mock executable %d' % (workflow_name,
                                                       executable_number),
                       description='N/A',
                       executable_path='/data/mock_executable.sh',
                       pbs_queue=pbs_queue,
                       pbs_processor=pbs_processor,
                       pbs_walltime=pbs_walltime)
        executable_number = executable_number + 1
        mock_executable.save()

        for k,node in workflow_spec.states.items():
            node['enqueued_class'] = app_models.ReferenceSet
    
            if node['class'] is None:
                node['class'] = app_strategies.IngestReferenceSetStrategy          
            queue = JobQueue(name='%s queue %d' % (workflow_name,
                                                   queue_number),
                             job_strategy_class=node['class'],
                             enqueued_object_class=node['enqueued_class'],
                             executable=mock_executable)
            queue_number = queue_number + 1

            queue.save()

            batch_size = 1
            max_retries = 1

            workflow_node = WorkflowNode(job_queue=queue,
                                         is_head=False,
                                         workflow=workflow,
                                         batch_size=batch_size,
                                         max_retries=max_retries) 
            workflow_node.save()


def xtest_from_yaml_file(workflow_config):
    wc = workflow_config.from_yaml_file(os.path.join(os.path.dirname(__file__),
                                        'workflows.yml'))

    print("\n")
    for w in wc:
        print("\nworkflow: " + w.name)
        for k in w.states.keys():
            s = w.states[k]
            line = [k, ' ', s['label']]
            if s['class'] is not None:
                line.extend([' (', s['class'], ')'])
            if s['manual']:
                line.append(' (m)')
            if s['workflow']:
                line.append(' (w)')
            print(''.join(line))
