from rest_framework import serializers

from dataset.models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'workflow_stage', 'status', 'project_name', 'summary', 
            'sample_size', 'scanner_type', 'accession_number', 
            'acknowledgements', 'license_title', 'license_url', 'curated' 
        ]
