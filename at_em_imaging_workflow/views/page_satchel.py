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
from django.core.exceptions import ObjectDoesNotExist
from development.models.microscope import Microscope
from development.models.e_m_montage_set import EMMontageSet
from workflow_engine.models.job_queue import JobQueue
from development.models.chunk import Chunk


context = {
    'pages': HEADER_PAGES,
}

def manual_qc_query(result):
    return result

def manual_qc_select(result):
    return result

def manual_qc_update(result):
    return result

def find_sections(result, get_params):
    workflow = get_params.get('workflow', None)

    if workflow:
        queues = JobQueue.objects.filter(
            workflownode__workflow__name=workflow)
    else:
        queues = JobQueue.objects.all()

    look_for = get_params.get('zs').split(',')
    print("look for: " + str(look_for))

    em_msets = EMMontageSet.objects.filter(
        section__z_index__in=look_for)

    result['message'] = {}
    idx = 0

    print("QUEUES: " + str(len(queues)))

    for q in queues:
        print("queue: " + q.name)
        em_mset_ids = [m.id for m in em_msets]

        jobs = Job.objects.filter(
            workflow_node__job_queue=q,
            enqueued_object_id__in=em_mset_ids)

        for j in jobs:
            m = [mset for mset in em_msets if mset.id == j.enqueued_object_id][0]
            
            result['message'][idx] = {
                'z': m.section.z_index,
                'run state': j.run_state.name,
                'acquisition': m.acquisition_date,
                'montage set id': m.id,
                'job queue': str(j.workflow_node)
                }
            idx = idx + 1

    result['success'] = True
    return result

def reimaged_sections(result, get_params):
    specimen = get_params.get('specimen')

    em_msets = EMMontageSet.objects.filter(
        section__specimen__uid=specimen)

    result['success'] = True
    result['message'] = {
        s.id: {
            'z': s.section.z_index,
            'acquisition': s.acquisition_date,
            } for s in em_msets }

def temca_query(result, get_params):
    scope_name = get_params.get('scope')

    # scope = Microscope.objects.filter(uid=scope_name)

    em_msets = EMMontageSet.objects.filter(
        microscope__uid=scope_name)

    result['success'] = True,
    result['message'] = {
            scope_name: {
                s.id: {
                    'scope': scope_name,
                    'EM montage id': s.id,
                    'acquisition': s.acquisition_date,
                    'specimen': s.section.specimen.uid,
                    'z': s.section.z_index } for s in em_msets}
        }

    return result

def all_chunks(result, get_params):
    chunks = Chunk.objects.all()

    chunk_start_indices = sorted(chunks, key=lambda c: c.computed_index)

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

    result['success'] = True,
    result['message'] = {}

    result['message']['chunk_size'] = settings.CHUNK_DEFAULTS['chunk_size']
    result['message']['chunk_sections'] = completed_sections

    return result


def page_satchel(request, url=None):
    success = False
    message = 'Nothing happened.'
    result = {
        'success': success,
        'message': message }
    
    query_handlers = {
        'manual_qc_query': manual_qc_query,
        'manual_qc_select': manual_qc_select,
        'manual_qc_update': manual_qc_update,
        'temca_query': temca_query,
        'reimaged_sections': reimaged_sections,
        'find_sections': find_sections,
        'all_chunks': all_chunks
    }

    try:
        query_name= request.GET.get('q')

        query_fn = query_handlers[query_name]

        result = query_fn(result, request.GET)
    except ObjectDoesNotExist as e:
        result['success'] = False
        result['message'] = "Object does not exist"
    except Exception as e:
        result['success'] = False
        result['message'] = str(e) + ' - ' + str(traceback.format_exc())

    return JsonResponse(result)


def page_satchel_old(request, url=None):
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
