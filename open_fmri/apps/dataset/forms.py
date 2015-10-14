import requests

from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput

from dataset.models import Dataset, Investigator, PublicationPubMedLink, \
    PublicationDocument, Task


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
