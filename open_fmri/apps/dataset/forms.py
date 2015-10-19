import requests

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit

from dataset.models import Dataset, FeaturedDataset, Investigator, \
    PublicationPubMedLink, PublicationDocument, Task


class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = [
            'workflow_stage', 'project_name', 'summary', 'sample_size', 
            'scanner_type', 'accession_number', 'acknowledgements', 
            'license_title', 'license_url', 'aws_link_title', 'aws_link_url' 
        ]
        
        widgets = {
            'license_url': TextInput(),
            'aws_link_url': TextInput()
        }

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

class TaskForm(ModelForm):
    cogat_id = forms.ChoiceField()

    class Meta:
        model = Task
        fields = ['cogat_id', 'number']

    def get_cogat_tasks(self):
        cogat_tasks = requests.get('http://cognitiveatlas.org/api/v-alpha/task')
        tasks_json = cogat_tasks.json()
        tasks_choices = []
        for elem in tasks_json:
            tasks_choices.append((elem['id'], elem['name']))
        
        return tasks_choices

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['cogat_id'].choices = self.get_cogat_tasks()

InvestigatorFormSet = inlineformset_factory(
    Dataset, Investigator, form=InvestigatorForm, extra=1)

PublicationDocumentFormSet = inlineformset_factory(
    Dataset, PublicationDocument, form=PublicationDocumentForm, extra=1) 

PublicationPubMedLinkFormSet = inlineformset_factory(
    Dataset, PublicationPubMedLink, form=PublicationPubMedLinkForm, extra=1)
    
TaskFormSet = inlineformset_factory(
    Dataset, Task, form=TaskForm, extra=1)

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
