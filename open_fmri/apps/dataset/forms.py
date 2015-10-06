from django.forms import ModelForm
from django.forms.widgets import TextInput

from dataset.models import Dataset


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
