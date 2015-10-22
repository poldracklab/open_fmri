import requests

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Column, Field, Fieldset, \
    Layout, Row, Submit

from dataset.models import Dataset, FeaturedDataset, Investigator, \
    PublicationPubMedLink, PublicationDocument, Revision, Task

class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = [
            'workflow_stage', 'status', 'project_name', 'summary', 
            'sample_size', 'scanner_type', 'accession_number', 
            'acknowledgements', 'license_title', 'license_url'  
        ]
        
        widgets = {
            'license_url': TextInput(),
            'aws_link_url': TextInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('workflow_stage', css_class="form-control"),
            Field('status', css_class="form-control"),
            Field('project_name', css_class="form-control"),
            Field('summary', css_class="form-control", rows=3),
            Field('sample_size', css_class="form-control"),
            Field('scanner_type', css_class="form-control", rows=1),
            Field('accession_number', css_class="form-control"),
            Field('acknowledgements', css_class="form-control", rows=3),
            Field('license_title', css_class="form-control"),
            Field('license_url', css_class="form-control"),
        )
        self.helper.form_tag = False

class UserDatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = [
            'project_name', 'summary', 'sample_size', 'scanner_type', 
            'acknowledgements'
        ]
    
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('project_name', css_class="form-control"),
            Field('summary', css_class="form-control", rows=3),
            Field('sample_size', css_class="form-control"),
            Field('scanner_type', css_class="form-control", rows=1),
            Field('accession_number', css_class="form-control"),
            Field('acknowledgements', css_class="form-control", rows=3),
        )
        self.helper.form_tag = False


class InvestigatorForm(ModelForm):
    class Meta:
        model = Investigator
        fields = ['investigator']

class PublicationDocumentForm(ModelForm):
    class Meta:
        model = PublicationDocument
        fields = ['document']

class PublicationPubMedLinkForm(ModelForm):
    class Meta:
        model = PublicationPubMedLink
        fields = ['title', 'url']

        widgets = {
            'url': TextInput()
        }

class RevisionForm(ModelForm):
    class Meta:
        model = Revision
        fields = ['revision_number', 'notes', 'aws_link_title', 'aws_link_url']
        widgets = {
            'aws_link_url': TextInput()
        }

class TaskForm(ModelForm):
    cogat_id = forms.ChoiceField()

    class Meta:
        model = Task
        fields = ['cogat_id', 'number']

    def get_cogat_tasks(self):
        cogat_tasks = requests.get('http://cognitiveatlas.org/api/v-alpha/task')
        tasks_json = cogat_tasks.json()
        tasks_choices = [("", "---------")]
        for elem in tasks_json:
            tasks_choices.append((elem['id'], elem['name']))
        
        return tasks_choices

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['cogat_id'].choices = self.get_cogat_tasks()

InvestigatorFormSet = inlineformset_factory(
    Dataset, Investigator, form=InvestigatorForm, extra=1, can_delete=True)

PublicationDocumentFormSet = inlineformset_factory(
    Dataset, PublicationDocument, form=PublicationDocumentForm, extra=1, 
    can_delete=True) 

PublicationPubMedLinkFormSet = inlineformset_factory(
    Dataset, PublicationPubMedLink, form=PublicationPubMedLinkForm, extra=1, 
    can_delete=True)
    
RevisionFormSet = inlineformset_factory(
    Dataset, Revision, form=RevisionForm, extra=1, can_delete=True)

TaskFormSet = inlineformset_factory(
    Dataset, Task, form=TaskForm, extra=1, can_delete=True)

class InvestigatorFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InvestigatorFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "",
                Field('investigator', css_class="form-control"),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            )
        )
        self.form_tag = False

class PublicationDocumentFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PublicationDocumentFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "Publication Document",
                Field('document', css_class="form-control"),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            )
        )
        self.form_tag = False

class PublicationPubMedLinkFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PublicationPubMedLinkFormSetHelper, self).__init__(*args, 
            **kwargs)
        self.layout = Layout(
            Fieldset(
                "PubMed Link",
                Field('title', css_class="form-control"),
                Field('url', css_class="form-control"),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            )
        )
        self.form_tag = False

class RevisionFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RevisionFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "Revision Information",
                Field('revision_number', css_class="form-control"),
                Column(
                    Field('aws_link_title', css_class="form-control"),
                    Field('aws_link_url', css_class="form-control"),
                ),
                Field('notes', css_class="form-control", rows=3),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            ),
        )
        self.form_tag = False

class TaskFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TaskFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "Cognitive Atlas Task",
                Field('cogat_id', css_class="form-control"),
                Field('number', css_class="form-control"),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            ),
        )
        self.form_tag = False

class FeaturedDatasetForm(ModelForm):
    class Meta:
        model = FeaturedDataset
        fields = ['dataset', 'image', 'title', 'content']
    
    def __init__(self, *args, **kwargs):
        super(FeaturedDatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('dataset', css_class="form-control"),
            Field('title', css_class="form-control"),
            Field('image', css_class="form-control"),
            Field('content', css_class="form-control"),
        )
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Featured Dataset'))




