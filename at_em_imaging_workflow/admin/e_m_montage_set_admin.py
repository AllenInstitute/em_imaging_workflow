from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from workflow_engine.models.configuration import Configuration
from django.urls import reverse
from django.utils.safestring import mark_safe
from workflow_engine.models.well_known_file import WellKnownFile
from workflow_engine.workflow_controller import WorkflowController
from development.models.e_m_montage_set import EMMontageSet
import simplejson as json
from development.models.chunk import Chunk


def redo_point_match_0_5(modeladmin, request, queryset):
    redo_point_match_0_5.short_description = \
        "Redo point match 0.5"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.update_point_match_state({
                'render_scale': 0.5
            })
            em_mset.object_state='PROCESSING'
            em_mset.save()

            WorkflowController.start_workflow(
                'em_2d_montage',
                em_mset,
                start_node_name='2D Montage Point Match',
                reuse_job=True,
                raise_priority=True)

def redo_point_match_0_6(modeladmin, request, queryset):
    redo_point_match_0_6.short_description = \
        "Redo point match 0.6"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.update_point_match_state({
                'render_scale': 0.6
            })
            em_mset.object_state='PROCESSING'
            em_mset.save()

            WorkflowController.start_workflow(
                'em_2d_montage',
                em_mset,
                start_node_name='2D Montage Point Match',
                reuse_job=True,
                raise_priority=True)

def redo_point_match_filter(modeladmin, request, queryset):
    redo_point_match_filter.short_description = \
        "Redo point match filter"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.update_point_match_state({
                'default_lambda': 1000.0,
                'transformation': 'Polynomial2DTransform',
                'poly_order': 2,
                'poly_factors': [1e-5, 1.0, 1e6]
            })
            em_mset.redo_processing()
            em_mset.save()

            WorkflowController.start_workflow(
                'filter_point_matches',
                em_mset,
                start_node_name='Filter Point Matches',
                reuse_job=True,
                raise_priority=True)

def redo_solver_5(modeladmin, request, queryset):
    redo_solver_5.short_description = \
        "Redo solver (Lambda=5.0)"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.get_em_2d_solver_lambda(5.0)
            em_mset.redo_solver()
            em_mset.save()

            WorkflowController.start_workflow(
                'em_2d_montage',
                em_mset,
                start_node_name='2D Montage Python Solver',
                reuse_job=True,
                raise_priority=True)

def redo_solver_100(modeladmin, request, queryset):
    redo_solver_100.short_description = \
        "Redo solver (Lambda=100.0)"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.get_em_2d_solver_lambda(100.0)
            em_mset.redo_solver()
            em_mset.save()

            WorkflowController.start_workflow(
                'em_2d_montage',
                em_mset,
                start_node_name='2D Montage Python Solver',
                reuse_job=True,
                raise_priority=True)

def redo_solver_1000(modeladmin, request, queryset):
    redo_solver_1000.short_description = \
        "Redo solver (Lambda=1000.0)"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.object_state = 'PROCESSING'
            em_mset.update_point_match_state({
                'default_lambda': 1000.0,
                'transformation': None,
                'poly_order': None
            })
            em_mset.save()

            WorkflowController.start_workflow(
                'em_2d_montage',
                em_mset,
                start_node_name='2D Montage Python Solver',
                reuse_job=True,
                raise_priority=True)

def swap_stacks(modeladmin, request, queryset):
    swap_stacks.short_description = "Swap Stacks"

    for em_mset in queryset.iterator():
        WorkflowController.start_workflow(
            'registration',
            em_mset,
            start_node_name='Swap Zs',
            reuse_job=True
        )

def reimage(modeladmin, request, queryset):
    reimage.short_description = \
        "Request Reimage"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.reimage()
            em_mset.save()

        WorkflowController.enqueue_next_queue_by_workflow_node(
            'em_2d_montage',
            em_mset,
            start_node_name='Manual QC / High Degree Polynomial or Point Match Regeneration')

def gap(modeladmin, request, queryset):
    gap.short_description = \
        "Gap"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.gap()
            em_mset.save()

def qc_pass_em_montage_set(modeladmin, request, queryset):
    qc_pass_em_montage_set.short_description = \
        "QC Pass selected montage sets"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.pass_qc()
            em_mset.save()

        WorkflowController.enqueue_next_queue_by_workflow_node(
            'em_2d_montage',
            em_mset,
            start_node_name='Manual QC / High Degree Polynomial or Point Match Regeneration')

def qc_fail_em_montage_set(modeladmin, request, queryset):
    qc_fail_em_montage_set.short_description = \
        "QC FAIL selected montage sets"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.fail_qc()
            em_mset.save()

def fail_em_montage_set(modeladmin, request, queryset):
    fail_em_montage_set.short_description = \
        "FAIL selected montage sets"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.fail()
            em_mset.save()

            # TODO: Fail or kill job in QC job queue

def reimage_not_select(modeladmin, request, queryset):
    reimage_not_select.short_description = \
        "Set state to REIMAGE_NOT_SELECTED"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.reimage_not_select()
            em_mset.save()


def reset_pending_em_montage_set(modeladmin, request, queryset):
    reset_pending_em_montage_set.short_description = \
        "reset selected montage sets to pending"

    if queryset:
        for em_mset in queryset.iterator():
            em_mset.object_state = 'PENDING'
            em_mset.save()

def assign_chunk(modeladmin, request, queryset):
    for em_mset in queryset:
        Chunk.assign_montage_set_to_chunks(em_mset)


class ConfigurationInline(GenericStackedInline):
    model=Configuration
    fields=('name', 'configuration_type', 'json_object')
    extra=0


class WellKnownFileInline(GenericStackedInline):
    model = WellKnownFile
    fields=('well_known_file_type',)
    ct_field='attachable_type'
    ct_fk_field='attachable_id'
    extra=0


class EMMontageSetAdmin(admin.ModelAdmin):
    change_list_template = 'admin/em_montage_set_change_list.html'
    search_fields = (
        'id',
        'section__z_index',
    )
    list_display = [
        'id',
        'z_index',
        'qc_link',
        'reimage_index',
        'reimage_count',
        'specimen_link',
        'microscope_link',
        'reference_set_link',
        'acquisition_date',
        'object_state',
        'load_uid'
    ]
    list_select_related = [
        'microscope',
        'reference_set',
        'section',
        'section__specimen',
        'sample_holder',
        'sample_holder__load',
    ]
    list_filter = [
        'section__specimen__uid',
        'microscope__uid',
        'object_state',
        'sample_holder__load',
    ]
    actions = [
        assign_chunk,
        redo_point_match_0_5,
        redo_point_match_0_6,
        redo_point_match_filter,
        redo_solver_5,
        redo_solver_100,
        redo_solver_1000,
        qc_pass_em_montage_set,
        qc_fail_em_montage_set,
        fail_em_montage_set,
        reimage,
        gap,
        swap_stacks,
        reset_pending_em_montage_set,
        reimage_not_select
    ]
    inlines = (ConfigurationInline,WellKnownFileInline)

    def load_uid(self, em_montage_set_object):
        try:
            l = em_montage_set_object.sample_holder.load
        except:
            return ''

        if l:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:development_load_change",
                        args=(l.pk,)),
                str(l.uid)))

    def microscope_link(self, em_montage_set_object):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:development_microscope_change",
                    args=(em_montage_set_object.microscope.pk,)),
            str(em_montage_set_object.microscope)))

    def specimen_link(self, em_montage_set_object):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:development_specimen_change",
                    args=(em_montage_set_object.section.specimen.pk,)),
            str(em_montage_set_object.section.specimen)))

    specimen_link.short_description = "Specimen"


    def qc_link_from_well_known_file(self, em_montage_set_object):
        if not em_montage_set_object.object_state in [
            EMMontageSet.STATE.EM_MONTAGE_SET_QC_PASSED,
            EMMontageSet.STATE.EM_MONTAGE_SET_QC_FAILED]:
            urls = '-'
        else:
            try:
                wkf = em_montage_set_object.well_known_files.filter(
                    well_known_file_type='defect_detection').first()
                filename = str(wkf)

                with open(filename) as j:
                    json_data = json.loads(j.read())
                    urls = ', '.join(
                        '<a target="qc" href="file:////{}">Plot</a>'.format(u)
                        for u in json_data['output_html']
                    )
            except:
                urls = '-'

        return mark_safe(urls)


    def qc_link(self, em_montage_set_object):
        if not em_montage_set_object.object_state in [
            EMMontageSet.STATE.EM_MONTAGE_SET_QC_PASSED,
            EMMontageSet.STATE.EM_MONTAGE_SET_QC_FAILED,
            EMMontageSet.STATE.EM_MONTAGE_SET_NOT_SELECTED]:
            urls = '-'
        else:
            try:
                qc_task = em_montage_set_object.jobs.get(
                    workflow_node__job_queue__name='Detect Defects',
                    archived=False).task_set.get()
                with open(qc_task.output_file) as j:
                    json_data = json.loads(j.read())
                    urls = ', '.join(
                        '<a target="qc" href="file:////{}">Plot</a>'.format(u)
                        for u in json_data['output_html']
                    )
            except:
                urls = 'error'

        return mark_safe(urls)

    def reimage_index(self, em_montage_set_object):
        return em_montage_set_object.reimage_index()

    def reimage_count(self, em_montage_set_object):
        return em_montage_set_object.section.montageset_set.count()


    def reference_set_link(self, em_montage_set_object):
        try:
            pk = em_montage_set_object.reference_set.pk
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:development_referenceset_change",
                        args=(pk,)),
                str(em_montage_set_object.reference_set)))
        except:
            return ''


    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        return response

    def lookup_allowed(self, key, value):
        if key in (
            'id__in',
            'section__z_index',
            'section__z_index__in',
            'section__z_index__gt',
            'section__z_index__gte',
            'section__z_index__lt',
            'section__z_index__lte'):
            return True

        return super(EMMontageSetAdmin, self).lookup_allowed(key, value)

