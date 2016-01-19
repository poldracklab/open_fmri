from datetime import datetime

from celery import shared_task, Celery

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('open_fmri')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(name='test_parse')
def test_parse():
    return datetime.now()
