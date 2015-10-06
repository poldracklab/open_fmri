from django.core.validators import URLValidator
from django.db import models

MAX_TITLE_LENGTH = 255

class Dataset(models.Model):
    
    
    WORKFLOW_STAGE_CHOICES = (
        ('SUBMITTED', 'Submitted'),
        ('IN_PROCESS', 'In Process'),
        ('STAGED', 'Staged'),
        ('SHARED', 'Shared'),
        ('REVIEW', 'Review')
    )
    workflow_stage = models.CharField(choices=WORKFLOW_STAGE_CHOICES,
                                      default='SUBMITTED', max_length=200)
    project_name = models.CharField(max_length=MAX_TITLE_LENGTH)
    summary = models.TextField()
    sample_size = models.IntegerField()
    scanner_type = models.TextField()
    accession_number = models.CharField(max_length=200)
    investigator = models.ManyToManyField('Investigator')
    acknowledgements = models.TextField()

    # These three fields are for any papers associated with the dataset
    publication_pubmed_link = models.ManyToManyField('PublicationPubMedLink')
    publication_full_text = models.ManyToManyField('PublicationFullText')
    publication_document = models.ManyToManyField('PublicationDocument')

    license_title = models.CharField(max_length=MAX_TITLE_LENGTH)
    license_url = models.TextField(validators=[URLValidator()])

    task = models.ManyToManyField('Task')

    aws_link_title = models.CharField(max_length=MAX_TITLE_LENGTH)
    aws_link_url = models.TextField(validators=[URLValidator()])

class Investigator(models.Model):
    investigator = models.CharField(max_length=200)

class PublicationPubMedLink(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.TextField(validators=[URLValidator()])
    
class PublicationFullText(models.Model):
    full_text = models.TextField()
    
class PublicationDocument(models.Model):
    document = models.FileField()

# Form will hit the cogat api, we will only record the cogat id for the task 
# so we can find it again and the name for display purposes
class Task(models.Model):
    cogat_id = models.TextField()
    name = models.TextField()
