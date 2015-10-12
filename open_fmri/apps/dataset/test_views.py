from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase

from model_mommy import mommy as ModelFactory

from dataset.models import Dataset

class DatasetViewTestCase(TestCase):
    
    def setUp(self):
        self.dataset = ModelFactory.make('Dataset')

        self.password = 'pass'
        self.user = User.objects.create_user(
            username='user', email='email@example.com', password=self.password)
        

    def test_list_view(self):
        response = self.client.get(reverse('dataset_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_view_nologin(self):
        response = self.client.get(reverse('dataset_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_view_login(self):
        self.assertTrue(self.client.login(
            username=self.user.username, password=self.password))
        response = self.client.get(reverse('dataset_create'))
        self.assertEqual(response.status_code, 200)


    def test_update_view_nologin(self):
        response = self.client.get(reverse('dataset_update', 
                                           args=[self.dataset.id]))
        self.assertEqual(response.status_code, 302)

    def test_update_view_login(self):
        self.assertTrue(self.client.login(
            username=self.user.username, password=self.password))
        response = self.client.get(reverse('dataset_update', 
                                           args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        response = self.client.get(reverse('dataset_detail', 
                                           args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)
