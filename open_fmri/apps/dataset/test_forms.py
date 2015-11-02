import random

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase

from model_mommy import mommy as ModelFactory

from dataset.forms import DatasetForm, InvestigatorForm, \
    PublicationDocumentForm, PublicationPubMedLinkForm, TaskForm, \
    UserDataRequestForm

from dataset.models import Dataset, Investigator, PublicationDocument, \
    PublicationPubMedLink, Task, UserDataRequest

class DatasetFormTestCase(TestCase):
    def test_valid_data(self):
        form = DatasetForm({
            'project_name': 'project name',
            'summary': 'summary',
            'sample_size': 2,
            'license_title': 'PPDL',
            'workflow_stage': 'SUBMITTED',
            'status': 'UNPUBLISHED'
        })
        self.assertTrue(form.is_valid())
        dataset = form.save()
        self.assertEqual(dataset.project_name, 'project name')
        self.assertEqual(dataset.summary, 'summary')
        self.assertEqual(dataset.sample_size, 2)
        self.assertEqual(dataset.license_title, 'PPDL')
        self.assertEqual(dataset.workflow_stage, 'SUBMITTED')
        self.assertEqual(dataset.status, 'UNPUBLISHED')

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
        form = PublicationPubMedLinkForm({})
        self.assertFalse(form.is_valid())

# Model factory doesn't generate a suitable choice for the choicefield, lets
# override the value it made.
class TaskTestCase(TestCase):
    def test_valid_data(self):
        task = ModelFactory.make('Task')
        blank_form = TaskForm()
        index = int(len(blank_form.fields['cogat_id'].choices) * 
            random.random())
        form = TaskForm({
            'cogat_id': blank_form.fields['cogat_id']._get_choices()[index][0],
            'number': task.number
        })
        self.assertTrue(form.is_valid())
    
    def test_blank_data(self):
        form = TaskForm({})
        self.assertFalse(form.is_valid())

class UserDataRequestTestCase(TestCase):
    def test_valid_data(self):
        user_data_request = ModelFactory.make('UserDataRequest')
        to_address = user_data_request.user_email_address
        form = UserDataRequestForm(
            {'user_email_address': to_address}
        )
        user_data_request = form.save()
        self.assertTrue(form.is_valid())
        self.assertIn(user_data_request.token, mail.outbox[0].body)
        self.assertIn(to_address, mail.outbox[0].to)

    def test_invalid_data(self):
        to_address = "not a real email address"
        form = UserDataRequestForm({'user_email_address': to_address})
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = UserDataRequestForm({})
        self.assertFalse(form.is_valid())
