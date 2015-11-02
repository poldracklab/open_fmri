from django.test import TestCase

from model_mommy import mommy as ModelFactory

from dataset.context_processors import featured_dataset_processor
from dataset.models import Dataset, FeaturedDataset

class FeaturedDatasetTestCase(TestCase):
    def test_no_featured_dataset(self):
        self.assertEquals({}, featured_dataset_processor(None))

    def test_extant_featured_dataset(self):
        dataset = ModelFactory.make('Dataset')
        featured_dataset = ModelFactory.make('FeaturedDataset')
        self.assertEquals(featured_dataset, 
                          featured_dataset_processor(None)['featured_dataset'])
