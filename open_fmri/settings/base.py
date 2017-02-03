import sys
import os
from os.path import join, abspath, dirname

from celery.schedules import crontab
from kombu import Exchange, Queue

# PATH vars
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

sys.path.insert(0, root('apps'))

ADMINS = (
    ('Ross Blair', 'rblair2@stanford.edu'),
)
MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = "admin@openfmri.org"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', False)
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '')




# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages'
)

PROJECT_APPS = (
    'dataset',
    'log_parse',
)

THIRD_PARTY_APPS = (
    'ckeditor',
    'crispy_forms',
    'opbeat.contrib.django',
    'rest_framework',
)

INSTALLED_APPS += PROJECT_APPS
INSTALLED_APPS += THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'dataset.context_processors.featured_dataset_processor',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'open_fmri.urls'

LOGIN_REDIRECT_URL = '/dataset/'

SITE_ID = 1

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'open_fmri.wsgi.application'


# Moved database settings into base since any testing we do within docker
# will be pulling from the same env file. Any non docker can override in 
# the relevant configuration file.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME', ''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', ''),
        'PORT': os.environ.get('POSTGRES_PORT', ''),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'  # 'Europe/London'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/var/www/static/'

MEDIA_ROOT = root('assets', 'uploads')
MEDIA_URL = '/media/'

LOGIN_URL = '/login/'

# Additional locations of static files

STATICFILES_DIRS = (
    root('assets'),
)

# If EMAIL_NOTIFY is set to true email notifications on dataset publish will
# be sent to news@openfmri.org
EMAIL_NOTIFY = os.environ.get("EMAIL_NOTIFY", False)
EMAIL_HOST = os.environ.get("EMAIL_HOST", '')
EMAIL_PORT = os.environ.get("EMAIL_PORT", '')
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", '')
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", '')

TWITTER_NOTIFY = os.environ.get("TWITTER_NOTIFY", False)
TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", '')
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", '')
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", '')
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET", '')

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.SessionAuthentication',
),}

CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
    },
}

OPBEAT = {
    'ORGANIZATION_ID': os.environ.get('OPBEAT_ORGANIZATION_ID', ''),
    'APP_ID': os.environ.get('OPBEAT_APP_ID', ''),
    'SECRET_TOKEN': os.environ.get('OPBEAT_SECRET_TOKEN', ''),
}

# Celery config
BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)

if os.environ.get('RUN_TASKS', False):
    CELERYBEAT_SCHEDULE = {
        'Parse Logs': {
            'task': 'log_parse_task',
            'schedule': crontab(minute='*', hour='8')
        },
    }

# slack endpoint URL to post json to for logging
LOG_ENDPOINT = os.environ.get('LOG_ENDPOINT', '')

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass


# importing test settings file if necessary
if len(sys.argv) > 1 and 'test' in sys.argv[1]:
    from .testing import *
