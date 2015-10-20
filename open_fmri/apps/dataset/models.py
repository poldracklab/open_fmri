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
    scanner_type = models.TextField(blank=True)
    accession_number = models.CharField(max_length=200, blank=True)
    acknowledgements = models.TextField(blank=True)

    # These three fields are for any papers associated with the dataset
    license_title = models.CharField(max_length=MAX_TITLE_LENGTH, 
                                     default="PPDL")
    license_url = models.TextField(validators=[URLValidator()], blank=True)

    aws_link_title = models.CharField(max_length=MAX_TITLE_LENGTH, blank=True)
    aws_link_url = models.TextField(validators=[URLValidator()], blank=True)
    
    def __str__(self):
        return self.project_name

class Investigator(models.Model):
    investigator = models.CharField(max_length=200)
    dataset = models.ForeignKey('Dataset')

class PublicationPubMedLink(models.Model):
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.TextField(validators=[URLValidator()])
    dataset = models.ForeignKey('Dataset')
    
class PublicationDocument(models.Model):
    document = models.FileField()
    dataset = models.ForeignKey('Dataset')

# Form will hit the cogat api, we will only record the cogat id for the task 
# so we can find it again and the name for display purposes
class Task(models.Model):
    cogat_id = models.TextField()
    name = models.TextField(blank=True)
    number = models.IntegerField()
    dataset = models.ForeignKey('Dataset')

class Revision(models.Model):
    previous_revision = models.ForeignKey('Revision', null=True)
    dataset = models.ForeignKey('Dataset')
    revision_number = models.CharField(max_length=200)
    notes = models.TextField()
    date_set = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.revision_number

    def save(self, *args, **kwargs):
        try:
            self.previous_revision = Revision.objects.filter(dataset=self.dataset).order_by('-date_set')[0]
        except:
            self.previous_revision = None
        super(Revision, self).save(*args, **kwargs)

class FeaturedDataset(models.Model):
    dataset = models.ForeignKey('Dataset')
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    content = models.TextField()
    date_featured = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
