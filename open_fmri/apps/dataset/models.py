import os
import re

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db import models
from django.template.loader import render_to_string

MAX_TITLE_LENGTH = 255

def acc_num_gen():
    """ Automatically generate accession numbers. """
    try:
        max_agg = Dataset.objects.all().aggregate(models.Max('accession_number'))
        max_val = max_agg['accession_number__max']
        match = re.search('\d+', max_val)
        int_val = int(max_val[match.span()[0]:match.span()[1]])
    except (TypeError, AttributeError):
        int_val = 0
    
    if int_val < 200:
        int_val = 200
    else:
        int_val += 1
    return "ds%06d" % (int_val)

def get_upload_path(instance, filename):
    return instance.dataset.accession_number + "/" + filename

class Contact(models.Model):
    """ Model for point of contact for a dataset """
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    website = models.TextField(validators=[URLValidator()], blank=True)
    
    def __str__(self):
        return self.name

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
    sample_size = models.IntegerField(blank=True, null=True)
    scanner_type = models.TextField(blank=True)
    accession_number = models.CharField(max_length=60, primary_key=True,
                                        default=acc_num_gen)
    acknowledgements = models.TextField(null=True, blank=True)
    
    license_title = models.CharField(max_length=MAX_TITLE_LENGTH, 
                                     default="PPDL")
    default_license_url = "http://opendatacommons.org/licenses/pddl/1.0/"
    license_url = models.TextField(validators=[URLValidator()], blank=True, 
                                   default=default_license_url)
    
    aws_link_title = models.CharField(max_length=MAX_TITLE_LENGTH, blank=True, 
                                      null=True)
    aws_link_url = models.TextField(validators=[URLValidator()], blank=True,
                                    null=True)
    contact = models.ForeignKey('Contact', blank=True, null=True)
    
    def __str__(self):
        return self.project_name

    def save(self, *args, **kwargs):
        notify = False
        if self.pk is not None:
            try:
                old_status = Dataset.objects.get(pk=self.pk).status
                if old_status == 'UNPUBLISHED' and self.status == 'PUBLISHED':
                    notify = True
            except ObjectDoesNotExist:
                pass
        else:
            if self.status == 'PUBLISHED':
                notify = True
        super(Dataset, self).save(*args, **kwargs)
        if notify:
            subject = "New dataset avaliable on OpenfMRI.org"
            body = render_to_string(
                "dataset/published_dataset_email_body.html", 
                {
                    'dataset': self, 
                    'url': reverse('dataset_detail', args=[self.pk])
                }
            )
            send_mail(subject, "", "news@openfmri.org", 
                      ["openfmri_pub@lists.stanford.edu"], html_message=body)

                

class FeaturedDataset(models.Model):
    dataset = models.ForeignKey('Dataset')
    date_featured = models.DateField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    
    def __str__(self):
        return self.title

class Investigator(models.Model):
    dataset = models.ForeignKey('Dataset')
    investigator = models.CharField(max_length=200)

class Link(models.Model):
    dataset = models.ForeignKey('Dataset')
    revision = models.ForeignKey('Revision', blank=True, null=True)
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.TextField(validators=[URLValidator()])

class PublicationDocument(models.Model):
    dataset = models.ForeignKey('Dataset')
    document = models.FileField(upload_to=get_upload_path)

    def __str__(self):
        return self.document.url

    def filename(self):
        return os.path.basename(self.document.name)

class PublicationPubMedLink(models.Model):
    dataset = models.ForeignKey('Dataset')
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.TextField(validators=[URLValidator()])

class Revision(models.Model):
    dataset = models.ForeignKey('Dataset')
    date_set = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    previous_revision = models.ForeignKey('Revision', null=True)
    revision_number = models.CharField(max_length=200)
    
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

class Task(models.Model):
    """
    ModelForm for Task will populate itself via the cogat api. Right now we 
    rebuild the url from the cogat_id, and the url field is unused.
    """
    dataset = models.ForeignKey('Dataset')
    cogat_id = models.TextField(null=True, blank=True)
    name = models.TextField(blank=True)
    number = models.IntegerField()
    url = models.TextField(validators=[URLValidator()], blank=True, null=True)
 
class UserDataRequest(models.Model):
    dataset = models.ForeignKey('Dataset', blank=True, null=True)
    request_sent = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=200, blank=True)
    user_email_address = models.EmailField()

    def __str__(self):
        return self.token
    
