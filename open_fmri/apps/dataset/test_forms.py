from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase

from model_mommy import mommy as ModelFactory

from dataset.forms import DatasetForm, InvestigatorForm, \
    PublicationDocumentForm, PublicationFullTextForm, PublicationPubMedLinkForm
from dataset.models import Dataset, Investigator, PublicationDocument, \
    PublicationFullText, PublicationPubMedLink

class DatasetFormTestCase(TestCase):
    def test_valid_data(self):
        form = DatasetForm({
            'project_name': 'project name',
            'summary': 'summary',
            'sample_size': 2,
            'license_title': 'PPDL',
            'workflow_stage': 'SUBMITTED'
        })
        self.assertTrue(form.is_valid())
        dataset = form.save()
        self.assertEqual(dataset.project_name, 'project name')
        self.assertEqual(dataset.summary, 'summary')
        self.assertEqual(dataset.sample_size, 2)
        self.assertEqual(dataset.license_title, 'PPDL')
        self.assertEqual(dataset.workflow_stage, 'SUBMITTED')

    def test_blank_data(self):
        form = DatasetForm({})
        self.assertFalse(form.is_valid())

class InvestigatorFormTestCase(TestCase):
    def test_valid_data(self):
        investigator = ModelFactory.make('Investigator')
        form = InvestigatorForm({'investigator': investigator.investigator})
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = DatasetForm({})
        self.assertFalse(form.is_valid())

class PublicaitonDocumentFormTestCase(TestCase):
    def test_valid_data(self):
        publication_document = ModelFactory.make('PublicationDocument')
        document = publication_document.document
        form = PublicationDocumentForm({},
            {'document': SimpleUploadedFile(document.name, document.read())})
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = PublicationDocumentForm({})
        self.assertFalse(form.is_valid())

class PublicationFullTextTestCase(TestCase):
    def test_valid_data(self):
        publication_full_text = ModelFactory.make('PublicationFullText')
        form = PublicationFullTextForm({
            'full_text': publication_full_text.full_text
        })
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = PublicationFullTextForm({})
        self.assertFalse(form.is_valid())

# the model factory doesn't take into account the non-standard validator we
# listed for the url field, well help it along for now
class PublicationPubMedLink(TestCase):
    def test_valid_data(self):
        publication_pubmed_link= ModelFactory.make('PublicationPubMedLink')
        form = PublicationPubMedLinkForm({
            'title': publication_pubmed_link.title,
            'url': "http://www.example.com"
        })
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = PublicationFullTextForm({})
        self.assertFalse(form.is_valid())


