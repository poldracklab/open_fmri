from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

celery = Celery('open_fmri')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
celery.config_from_object('django.conf:settings')
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
