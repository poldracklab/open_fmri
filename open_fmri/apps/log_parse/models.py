from django.db import models

class LogFile(models.Model):
    key = models.TextField(unique=True)
    parsed = models.BooleanField()
    lock = models.BooleanField()
    last_line_read = models.IntegerField(null=True)

class S3File(models.Model):
    filename = models.TextField(unique=True)
    count = models.IntegerField()
    dataset = models.ForeignKey('dataset.Dataset', null=True)
