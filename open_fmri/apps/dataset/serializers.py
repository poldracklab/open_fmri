from rest_framework import serializers

from dataset.models import Dataset, Investigator, Link, PublicationDocument, \
    PublicationPubMedLink, Revision, Task

class InvestigatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigator
        fields = ['investigator']

class LinkSerializer(serializers.ModelSerializer):
    revision = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Link
        fields = ['title', 'url', 'revision']

class PublicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationDocument
        fields = ['document']

class PublicationPubMedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationPubMedLink
        fields = ['title', 'url']

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['revision_number', 'notes', 'aws_link_title', 'aws_link_url']

class TaskSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['cogat_id', 'number', 'name', 'url']

    def get_url(self, task):
        return "http://www.cognitiveatlas.org/id/" + str(task.cogat_id)

class DatasetSerializer(serializers.ModelSerializer):
    
    investigator_set = InvestigatorSerializer(read_only=True, many=True)
    publicationdocument_set = serializers.StringRelatedField()
    publicationpubmedlink_set = PublicationPubMedLinkSerializer(read_only=True,
                                                                many=True)
    task_set = TaskSerializer(read_only=True, many=True)
    revision_set = RevisionSerializer(read_only=True, many=True)
    link_set = LinkSerializer(read_only=True, many=True)
    class Meta:
        model = Dataset
        fields = [
            'accession_number', 'project_name', 'summary', 
            'sample_size', 'scanner_type', 
            'acknowledgements', 'license_title', 'license_url', 'curated',
            'publicationdocument_set', 'publicationpubmedlink_set', 'task_set',
            'revision_set', 'investigator_set', 'link_set'
        ]
