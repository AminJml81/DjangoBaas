import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'AMINJLMDEVSECRET'
DEBUG = True
USE_TZ = True

ROOT_URLCONF = 'django_baas.urls'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.postgres',
    'rest_framework',
    'django_baas',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}