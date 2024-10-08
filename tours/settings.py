"""
Django settings for tours project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8$i*$o1l2f7g0=66433p3j5m$&g*^wy%7!x_6*@wfofa6*h3j0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'home',
    'dashboard',
    'widget_tweaks',
    'paypal.standard.ipn',
    'payment',
    'celery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tours.urls'

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

WSGI_APPLICATION = 'tours.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tours',
        'USER': 'postgres',
        'PASSWORD': 'qwerty',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        # 'PORT': '3306',
        'PORT': '5432',
    #     'OPTIONS': {
    #     'autocommit': True,
    # },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'thekenyanthrill@gmail.com'
EMAIL_HOST_PASSWORD = 'lookalive'
EMAIL_PORT = 587
ACCOUNT_ACTIVATION_DAYS = 2

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPOSITORY_ROOT = os.path.dirname(BASE_DIR)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(REPOSITORY_ROOT, 'static/')

MEDIA_URL = '/tours/dashboard/static/uploads/'
MEDIA_ROOT = os.path.join(REPOSITORY_ROOT, 'tours/dashboard/static/uploads/')

# LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'login_success'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-paypal settings
PAYPAL_RECEIVER_EMAIL = 'vicngetichvictor@gmail.com'
PAYPAL_TEST = True

# BT_ENVIRONMENT='sandbox',
# # BRAINTREE_PRODUCTION = False  # We'll need this later to switch between the sandbox and live account
# BRAINTREE_MERCHANT_ID = 'wzv3chvt3rgcnc7s',
# BRAINTREE_PUBLIC_KEY = 'v83krfwsbyxjxbwp',
# BRAINTREE_PRIVATE_KEY = '9643735fddd5db520c6b0791718895a1'

CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', 'application/text']
CELERY_TIMEZONE = 'Africa/Nairobi'
USE_THOUSAND_SEPARATOR = True