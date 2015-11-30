from django.core.urlresolvers import resolve
from django.test import TestCase

from model_mommy import mommy as ModelFactory

from dataset.models import Dataset, FeaturedDataset
from dataset.views import DatasetCreate, DatasetList, DatasetUpdate, \
    DatasetDelete, FeaturedDatasetEdit, FeaturedDatasetDelete

class DataSetUrlTestCase(TestCase):

    def setUp(self):
        self.dataset = Dataset.objects.create(
            project_name = 'project name',
            summary = 'project summary',
            accession_number = 'ds999999z',
            sample_size = 2
        )
        self.featured_dataset = ModelFactory.make('FeaturedDataset', dataset=self.dataset)
    
    def test_dataset_list(self):
        found = resolve('/dataset/')
        self.assertEqual(found.func.__name__, DatasetList.as_view().__name__)

    def test_dataset_create(self):
        found = resolve('/dataset/new/')
        self.assertEqual(found.func.__name__, DatasetCreate.as_view().__name__)

    def test_dataset_update(self):
        found = resolve('/dataset/edit/' + str(self.dataset.accession_number))
        self.assertEqual(found.func.__name__, DatasetUpdate.as_view().__name__)

    def test_dataset_delete(self):
        found = resolve('/dataset/delete/' + str(self.dataset.accession_number))
        self.assertEqual(found.func.__name__, DatasetDelete.as_view().__name__)
    
    def test_featureddataset_edit(self):
        found = resolve('/dataset/featured/')
        self.assertEqual(found.func.__name__, 
                         FeaturedDatasetEdit.as_view().__name__)

    def test_featureddataset_delete(self):
        found = resolve('/dataset/featured/delete/' + 
                        str(self.featured_dataset.id))
        self.assertEqual(found.func.__name__, 
                         FeaturedDatasetDelete.as_view().__name__)
