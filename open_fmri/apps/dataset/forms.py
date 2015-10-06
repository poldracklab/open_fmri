from django.forms import ModelForm

from dataset.models import Dataset

class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = [
            'workflow_stage', 'project_name', 'summary', 'sample_size', 
            'scanner_type', 'accession_number', 
            'acknowledgements', 'publication_pubmed_link', 
            'publication_full_text', 'publication_document', 'license_title', 
            'license_url', 'task', 'aws_link_title', 'aws_link_url' 
        ]
