from .common import *

DEBUG = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = 'https://despacho-cloud.s3-us-west-2.amazonaws.com/'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'despacho-cloud'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
MEDIA_URL = 'https://despacho-cloud.s3-us-west-2.amazonaws.com/media/'
MEDIA_ROOT = MEDIA_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DBNAME'),
        'USER': os.getenv('DBUSER'),
        'PASSWORD': os.getenv('DBPASSWORD'),
        'HOST': os.getenv('DBHOST'),
        'PORT': '5432',
    }
}