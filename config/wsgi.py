import os

from django.core.wsgi import get_wsgi_application

if os.getenv('SETTINGS', None) is not None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv('SETTINGS'))
else
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.develop")

application = get_wsgi_application()
