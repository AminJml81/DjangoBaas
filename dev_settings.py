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
    'rest_framework_simplejwt'
    'django_baas',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
