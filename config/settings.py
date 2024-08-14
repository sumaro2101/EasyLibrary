"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

from .utils import find_env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = find_env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = find_env('TEST')

ALLOWED_HOSTS = [find_env('ALLOWED_HOSTS'), 'localhost']

SWAGGER_SETTINGS = {
    'VALIDATOR_URL': 'http://127.0.0.1:8000'
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # cachalot
    'cachalot',
    # rest-framework
    'rest_framework',
    # django-filter
    'django_filters',
    # redoc
    'drf_yasg',
    # celery
    'django_celery_beat',
    # django-phone,
    'phonenumber_field',
    # CORS
    'corsheaders',
    # django_extensions
    'django_extensions',
    # django_toolbar
    'debug_toolbar',
    # custom_apps
    'users.apps.UsersConfig',
    'library.apps.LibraryConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django_debug_toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

TEMPLATES_TO_TASK = {
    'ORDER_OPEN': 'library/template_order.html',
    'ORDER_CLOSE': 'library/template_order_close.html',
    'EXTENSION_OPEN': 'library/template_extension_open.html',
    'EXTENSION_ACCEPT': 'library/template_accept.html',
    'EXTENSION_CANCEL': 'library/template_cancel.html'
}

WSGI_APPLICATION = 'config.wsgi.application'


# rest-framework

_page_paginator = 'rest_framework.pagination.PageNumberPagination'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': _page_paginator,
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1)
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


try:
    DOCKER_DEBUG = bool(int(find_env('DOCKER_DEBUG')))
except TypeError:
    DOCKER_DEBUG = True

if DOCKER_DEBUG:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : BASE_DIR / 'db.sqlite3'
        }
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': find_env('DB_NAME'),
        'HOST': 'db',
        'PORT': find_env('DB_PORT'),
        'USER': find_env('DB_USER'),
        'PASSWORD': find_env('DB_PASSWORD')
        }
    }


# CELERY

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND", "redis://127.0.0.1:6379/0")
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = find_env('DEFAULT_DATABASE_BEAT')

STANDART_HOUR_TO_TASK = 8
STANDART_MINUTE_TO_TASK = 0

TEMPLATE_PERIODICK_TASK_PATH = 'library/template_overdue.html'
MAIL_SUBJECT_TASK_PATH = 'library/mail_send_subject.txt'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# CORS

CORS_ALLOWED_ORIGINS = ['http://localhost:8000']

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']

CORS_ALLOW_ALL_ORIGINS = False

if not DOCKER_DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': find_env('REDIS_CACHE'),
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Omsk'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"


# Media files

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


EMAIL_HOST = find_env('YANDEX_HOST')
EMAIL_PORT = find_env('YANDEX_PORT')
EMAIL_HOST_USER = find_env('YANDEX_HOST_USER')
EMAIL_HOST_PASSWORD = find_env('YANDEX_PASSWORD_HOST')
EMAIL_USE_SSL = True if find_env('YANDEX_CONNTECT_TYPE') == 'SSL' else False
EMAIL_USE_TLS = True if find_env('YANDEX_CONNTECT_TYPE') == 'TLS' else False

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
