from django.db import models

class LogFile(models.Model):
    key = models.TextField()
    parsed = models.BooleanField()
    lock = models.BooleanField()
    last_line_read = models.IntegerField(null=True)

class S3File(models.Model):
    url = models.URLField()
    count = models.IntegerField()
