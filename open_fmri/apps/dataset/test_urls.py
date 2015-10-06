from django.core.urlresolvers import resolve
from django.test import TestCase

from dataset.models import Dataset
from dataset.views import DatasetCreate, DatasetList, DatasetUpdate

class DataSetUrlTest(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            project_name = 'project name',
            summary = 'project summary',
            sample_size = 2
        )
    
    def test_dataset_list(self):
        found = resolve('/dataset/')
        self.assertEqual(found.func.__name__, DatasetList.as_view().__name__)

    def test_dataset_create(self):
        found = resolve('/dataset/new/')
        self.assertEqual(found.func.__name__, DatasetCreate.as_view().__name__)

    def test_dataset_update(self):
        found = resolve('/dataset/edit/' + str(self.dataset.id))
        self.assertEqual(found.func.__name__, DatasetUpdate.as_view().__name__)
