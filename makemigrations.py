import django
from django.conf import settings
from django.core.management import call_command


# minimum django settings for identifying package
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django_baas',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

django.setup()


if __name__ == '__main__':
    call_command('makemigrations', 'django_baas')