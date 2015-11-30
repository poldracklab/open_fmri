import os

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
    STATUS_CHOICES = (
        ('PUBLISHED', 'Published'),
        ('UNPUBLISHED', 'Unpublished')
    )
    workflow_stage = models.CharField(choices=WORKFLOW_STAGE_CHOICES,
                                      default='SUBMITTED', max_length=200)
    status = models.CharField(choices=STATUS_CHOICES, default='UNPUBLISHED', 
                              max_length=200)
    curated = models.NullBooleanField(default=False, null=True)
    project_name = models.CharField(max_length=MAX_TITLE_LENGTH)
    summary = models.TextField(null=True)
    sample_size = models.IntegerField()
    scanner_type = models.TextField(blank=True)
    accession_number = models.CharField(max_length=60, primary_key=True)
    acknowledgements = models.TextField(null=True, blank=True)
    
    # These three fields are for any papers associated with the dataset
    license_title = models.CharField(max_length=MAX_TITLE_LENGTH, 
                                     default="PPDL")
    default_license_url = "http://opendatacommons.org/licenses/pddl/1.0/"
    license_url = models.TextField(validators=[URLValidator()], blank=True, 
                                   default=default_license_url)
    
    aws_link_title = models.CharField(max_length=MAX_TITLE_LENGTH, blank=True, 
                                      null=True)
    aws_link_url = models.TextField(validators=[URLValidator()], blank=True,
                                    null=True)
    
    def __str__(self):
        return self.project_name

class Investigator(models.Model):
    investigator = models.CharField(max_length=200)
    dataset = models.ForeignKey('Dataset')

class PublicationPubMedLink(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.TextField(validators=[URLValidator()])
    dataset = models.ForeignKey('Dataset')

def get_upload_path(instance, filename):
    return instance.dataset.accession_number + "/" + filename

class PublicationDocument(models.Model):
    document = models.FileField(upload_to=get_upload_path)
    dataset = models.ForeignKey('Dataset')

    def __str__(self):
        return self.document.url

    def filename(self):
        return os.path.basename(self.document.name)

# Form will hit the cogat api, we will only record the cogat id for the task 
# so we can find it again and the name for display purposes
class Task(models.Model):
    cogat_id = models.TextField(null=True, blank=True)
    name = models.TextField(blank=True)
    url = models.TextField(validators=[URLValidator()], blank=True, null=True)
    number = models.IntegerField()
    dataset = models.ForeignKey('Dataset')

    def get_url(self):
        return "http://www.cognitiveatlas.org/id/" + self.cogat_id

class Revision(models.Model):
    previous_revision = models.ForeignKey('Revision', null=True)
    dataset = models.ForeignKey('Dataset')
    revision_number = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    date_set = models.DateTimeField(auto_now_add=True)
    
    aws_link_title = models.CharField(max_length=MAX_TITLE_LENGTH, blank=True)
    aws_link_url = models.TextField(validators=[URLValidator()], blank=True)
    
    def __str__(self):
        return self.revision_number

    def save(self, *args, **kwargs):
        try:
            self.previous_revision = Revision.objects.filter(dataset=self.dataset).order_by('-date_set')[0]
        except:
            self.previous_revision = None
        super(Revision, self).save(*args, **kwargs)

class Link(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.TextField(validators=[URLValidator()])
    dataset = models.ForeignKey('Dataset')
    revision = models.ForeignKey('Revision', blank=True, null=True)

class FeaturedDataset(models.Model):
    dataset = models.ForeignKey('Dataset')
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    content = models.TextField()
    date_featured = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class UserDataRequest(models.Model):
    user_email_address = models.EmailField()
    request_sent = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=200, blank=True)
    
