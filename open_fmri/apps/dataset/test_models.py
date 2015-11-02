from django.test import TestCase

from model_mommy import mommy as ModelFactory

from dataset.models import Dataset, Revision

class RevisionTestCase(TestCase):
    def setUp(self):
        self.dataset = ModelFactory.make('Dataset')
        self.revision_1 = ModelFactory.make('Revision', dataset=self.dataset)

    def test_one_revision(self):
        self.assertEqual(len(Revision.objects.all()), 1)
        self.assertIsNone(self.revision_1.previous_revision)
        self.assertEqual(self.revision_1.revision_number, self.revision_1.__str__())

    def test_two_revisions(self):
        revision_2 = ModelFactory.make('Revision', dataset=self.dataset)
        self.assertEqual(revision_2.previous_revision, self.revision_1)
