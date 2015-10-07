from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput

from dataset.models import Dataset, Investigator, PublicationPubMedLink, \
    PublicationFullText, PublicationDocument


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

class PublicationFullTextForm(ModelForm):
    class Meta:
        model = PublicationFullText
        fields = ['full_text']

class PublicationPubMedLinkForm(ModelForm):
    class Meta:
        model = PublicationPubMedLink
        fields = ['title', 'url']

        widgets = {
            'url': TextInput()
        }

InvestigatorFormSet = inlineformset_factory(
    Dataset, Investigator, form=InvestigatorForm, extra=1)

PublicationDocumentFormSet = inlineformset_factory(
    Dataset, PublicationDocument, form=PublicationDocumentForm, extra=0, 
    can_delete=False)

PublicationFullTextFormSet = inlineformset_factory(
    Dataset, PublicationFullText, form=PublicationFullTextForm, extra=0, 
    can_delete=False)

PublicationPubMedLinkFormSet = inlineformset_factory(
    Dataset, PublicationPubMedLink, form=PublicationPubMedLinkForm, extra=0, 
    can_delete=False)

