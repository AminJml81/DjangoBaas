import django
from django.conf import settings
from django.core.management import call_command
import os


# minimum django settings for identifying packages.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_settings')

django.setup()


if __name__ == '__main__':
    call_command('makemigrations', 'django_baas')