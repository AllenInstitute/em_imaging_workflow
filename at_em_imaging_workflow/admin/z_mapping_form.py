from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from workflow_engine.models import Configuration
from workflow_engine.workflow_controller import WorkflowController
import os


class ZMappingForm(ModelForm):
    xls_path = forms.CharField(max_length=1024, help_text='file name')

    def __init__(self, *args, **kwargs):
        self.xls_path = kwargs.pop('xls_path', None)

        super(ZMappingForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Configuration
        fields=('name', 'xls_path', 'json_object')
        extra=0

    def clean_xls_path(self):
        self.xls_path = self.cleaned_data.get('xls_path', 0)

        if not os.path.exists(self.xls_path):
            raise ValidationError("spreadsheet not found at specified path")

        return self.xls_path

    def clean_configuration_type(self):
        return "z_mapping"

    def save(self, commit=True):
        config_object = super(ZMappingForm, self).save()

        load_object = config_object.content_object

        tape = load_object.uid

        tape_df = load_object.read_mapping_spreadsheet(
            self.xls_path,
            sheet=tape
        )

        tape_df = tape_df[
            tape_df['Barcode'].notnull() &
            tape_df['Z'].notnull() &
            (tape_df['Z and TAO agree?'] == True)]

        config_object.name = '{} Z Mapping'.format(tape)
        config_object.configuration_type = 'z_mapping'
        config_object.json_object = {
            str(load_object.offset + barcode): int(perm_z)
            for (_, barcode, perm_z)
            in tape_df.loc[:,['Barcode','Z']].itertuples()
        }

        if commit:
            config_object.save()

        WorkflowController.start_workflow(
            'em_2d_montage',
            load_object,
            start_node_name='Load Z Mapping',
            reuse_job=True)

        # TODO: enqueue the load object in wait for z mapping
        return config_object
