import os
import sys
from decouple import config
from dj_database_url import parse as db_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_nose',
    'django.contrib.staticfiles',
    'diegorocha.curriculo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'diegorocha.curriculo.middlewares.VersionMiddleware',
]

ROOT_URLCONF = 'diegorocha.urls'

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
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'diegorocha.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        cast=db_url)
}

if 'test' in sys.argv or 'test_coverage' in sys.argv:  # Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

VERSION_CODE = config('VERSION_CODE', default='dev')
VERSION_CODE_HEADER = config('VERSION_CODE_HEADER', default='X-Version')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_S3 = config('STATIC_S3', cast=bool, default=False)
if STATIC_S3:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='diegorocha-static')
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=31536000",
    }
    AWS_IS_GZIPPED = True
    AWS_LOCATION = VERSION_CODE
    AWS_QUERYSTRING_AUTH = config('AWS_QUERYSTRING_AUTH', cast=bool, default=False)
    STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{VERSION_CODE}/'
else:
    STATIC_URL = config('STATIC_URL', default='/static/')
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')


# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

USE_ETAGS = True

ADMINS = (('Diego Rocha', 'diego@diegorocha.com.br'), )

if config('USE_SMTP', default=False, cast=bool):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
    EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
