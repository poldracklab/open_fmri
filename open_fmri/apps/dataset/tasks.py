import datetime

from celery import shared_task, Celery

app = Celery('open_fmri')
app.config_from_object('django.conf:settings.base')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(name='test_parse')
def test_parse():
    logger = test_parse.get_logger()
    logger.info(str(datetime.now))
    return datetime.now()

