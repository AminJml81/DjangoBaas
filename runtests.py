import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_settings')

django.setup()

if __name__ == '__main__':
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['django_baas'])
    sys.exit(bool(failures))