"""
Django settings for at_em_imaging_workflow project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = BASE_DIR

BASE_FILE_PATH = \
    '/allen/programs/celltypes/workgroups/array_tomography/blue_sky/files/'
PBS_FINISH_PATH = \
    '/allen/programs/celltypes/workgroups/array_tomography/blue_sky' + \
    '/at_em_imaging_workflow/pbs_execution_finish.py'

MESSAGE_QUEUE_NAME = 'at_em_imaging_workflow'
CELERY_MESSAGE_QUEUE_NAME = 'celery_' + MESSAGE_QUEUE_NAME
MESSAGE_QUEUE_USER = 'blue_sky_user'
MESSAGE_QUEUE_PASSWORD = 'blue_sky_user'
MESSAGE_QUEUE_PORT = 5672

FIJI_PATH = \
    '/allen/aibs/shared/image_processing/volume_assembly' + \
    '/Fiji.app/ImageJ-linux64'
GRID_SIZE = 3
HEAP_SIZE = 10
INITIAL_SIGMA = 1.6
STEPS = 3
MIN_OCTAVE_SIZE = 800
MAX_OCTAVE_SIZE = 1200
FD_SIZE = 4
FD_BINS = 8

ROD = 0.92
MAX_EPSILON = 50
MIN_INLIER_RATIO = 0.0
MIN_NUMBER_INLIERS = 5
EXPECTED_MODEL_INDEX = 1
MULTIPLE_HYPOTHESES = True
REJECT_IDENTITY = True
IDENTITY_TOLERANCE = 5.0
TILES_ARE_IN_PLACE = True
DESIRED_MODEL_INDEX = 0
REGULARIZE = False
MAX_ITERATIONS_OPTIMIZE = 2000
MAX_PLATEAU_WIDTH_OPTIMIZE = 200
DIMENSION = 5
LAMBDA_VAL = 0.01
CLEAR_TRANSFORM = True
VISUALIZE = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qde=#m)tepmm$!n1j3+b8#!mz_s-pn2@2soe@9^_ol8363pjlp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

RESULTS_PER_PAGE = 20

MAX_DISPLAYED_PAGE_LINKS = 10

WORKFLOW_VERSION = 0.1

MESSAGE_QUEUE_HOST = 'ibs-roby-vm1'

MILLISECONDS_BETWEEN_REFRESH = 10000
# MILLISECONDS_BETWEEN_REFRESH = 1000

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'workflow_engine',
    'development'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'at_em_imaging_workflow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'at_em_imaging_workflow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'at_em_imaging_workflow',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'devdb2',
        'PORT': '5942'
    },
    'TEST': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'database.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
        'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Pacific'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/logs/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

try:
    with open(os.path.join(
        os.path.dirname(__file__), "local_settings.py"
    )) as ls:
        exec(ls.read())
except IOError:
    pass
