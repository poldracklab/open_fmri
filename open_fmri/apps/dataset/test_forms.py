from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase

from dataset.forms import DatasetForm
from dataset.models import Dataset

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
