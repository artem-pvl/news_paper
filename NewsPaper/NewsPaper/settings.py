"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from .secret import EMAIL_FOR_SEND, EMAIL_FOR_SEND_PASS

import logging


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8!7mwa0*%8#m#j)+==^)*3_m4_@@az+ft*f$x7-g_$=_)+eka3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


def log_filter_debug_info(rec: logging.LogRecord):
    return (rec.levelname == 'DEBUG') or (rec.levelname == 'INFO')


def log_filter_warning(rec: logging.LogRecord):
    return rec.levelname == 'WARNING'


def log_filter_error_critical(rec: logging.LogRecord):
    return (rec.levelname == 'ERROR') or (rec.levelname == 'CRITICAL')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'deb': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        'war': {
            'format': '{asctime} {levelname} {pathname} {message}',
            'style': '{',
        },
        'cri': {
            'format': '{asctime} {levelname} {pathname} {message} {exc_info}',
            'style': '{',
        },
        'to_file_general': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'only_debug_info': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': log_filter_debug_info,
        },
        'only_warning': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': log_filter_warning,
        },
        'only_error_critical': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': log_filter_error_critical,
        },
    },
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true', 'only_debug_info'],
            'class': 'logging.StreamHandler',
            'formatter': 'deb',
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true', 'only_warning'],
            'class': 'logging.StreamHandler',
            'formatter': 'war',
        },
        'console_critical': {
            'level': 'ERROR',
            'filters': ['require_debug_true', 'only_error_critical'],
            'class': 'logging.StreamHandler',
            'formatter': 'cri',
        },
        'file_general': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'to_file_general',
            'filename': './general.log'
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'cri',
            'filename': './errors.log'
        },
        'file_security': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'to_file_general',
            'filename': './security.log'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'war',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning',
                         'console_critical', 'file_general'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db_backends': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.flatpages',
    "news_paper.apps.NewsPaperConfig",
    'django_filters',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'NewsPaper.middlewares.TimezoneMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_'
        'validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGES = {
    ('ru', 'Russian'),
    ('en', 'English'),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/news/'
LOGOUT_REDIRECT_URL = '/news/'

ACCOUNT_LOGOUT_REDIRECT_URL = '/news/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_FORMS = {'signup': 'news_paper.forms.BasicSignupForm'}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = EMAIL_FOR_SEND
EMAIL_HOST_PASSWORD = EMAIL_FOR_SEND_PASS
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}
