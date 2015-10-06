from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase

from dataset.models import Dataset

# These are going to be real boring until we get users going.
class DatasetViewTestCase(TestCase):
    
    def setUp(self):
        self.dataset = Dataset.objects.create(
            project_name = 'project name',
            summary = 'project summary',
            sample_size = 2
        )

    def test_list_view(self):
        response = self.client.get(reverse('dataset_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_view(self):
        response = self.client.get(reverse('dataset_create'))
        self.assertEqual(response.status_code, 200)


    def test_list_view(self):
        response = self.client.get(reverse('dataset_update', 
                                           args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)
