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
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
import traceback
from django.template import loader
from workflow_engine.models.job import Job
from workflow_engine.models.workflow_node import WorkflowNode
from workflow_engine.models import ZERO, ONE
from workflow_engine.views import shared, HEADER_PAGES
from workflow_engine.workflow_controller import WorkflowController
from development.models.chunk import Chunk


context = {
    'pages': HEADER_PAGES,
}

def chunks_page(request, url=None):
    if url is None:
        url = request.get_full_path()

    chunks = Chunk.objects.all()
    chunk_start_indices = sorted(chunks, key=lambda c: c.computed_index)

    #context['chunks'] = chunk_start_indices
    #context['chunk_indices'] = range(settings.CHUNK_DEFAULTS['chunk_size'])

    completed_sections = []

    for chnk in chunk_start_indices:
        complete_state = []
        found_sections = [s.z_index for s in chnk.sections.all()]
        z_start, z_end = Chunk.calculate_z_range(chnk.computed_index)

        for z in range(z_start, z_end):
            if z in found_sections:
                complete_state.append({'z': z, 'complete': 'T'})
            else:
                complete_state.append({'z': z, 'complete': 'F' })

        completed_sections.append((
            chnk.computed_index,
            complete_state))

    context['chunk_size'] = settings.CHUNK_DEFAULTS['chunk_size']
    context['chunk_sections'] = completed_sections

    template = loader.get_template('chunks.html')

    return HttpResponse(template.render(context, request))
