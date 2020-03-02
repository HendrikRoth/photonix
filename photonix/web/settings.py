"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from pathlib import Path


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(Path(__file__).parent.parent.resolve())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r*z#sh2aqb!zjz#s7h@5&toyx@t_r4nfrgwg%r$4)2@d@8ypyb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('ENV', 'prd') != 'prd'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,[::1]').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'photonix.common',
    'photonix.photos',
    'photonix.web',
    'graphene_django',
    'django_filters',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'photonix.web.urls'

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

WSGI_APPLICATION = 'photonix.web.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'HOST':     os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'NAME':     os.environ.get('POSTGRES_DB', 'photonix'),
        'USER':     os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
    }
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'photos.User'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


if os.path.exists('/data'):
    DATA_DIR = str(Path('/data'))
else:
    DATA_DIR = str(Path(BASE_DIR).parent / 'data')

CACHE_DIR = str(Path(DATA_DIR) / 'cache')
MODEL_DIR = str(Path(DATA_DIR) / 'models')

STATIC_ROOT = str(Path(BASE_DIR) / 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = str(Path(BASE_DIR).parent / 'data')

THUMBNAIL_ROOT = str(Path(CACHE_DIR) / 'thumbnails')

THUMBNAIL_SIZES = [
    # Width, height, crop method, JPEG quality, whether it should be generated upon upload
    (256, 256, 'cover', 50, True),  # Square thumbnails
    # We use the largest dimension for both dimensions as they won't crop and some with in portrait mode 
    (960, 960, 'contain', 75, False),  # 960px
    (1920, 1920, 'contain', 75, False),  # 2k
    (3840, 3840, 'contain', 75, False),  # 4k
]


PHOTO_INPUT_DIRS = [str(Path(BASE_DIR).parent.parent / 'photos_to_import')]
PHOTO_OUTPUT_DIRS = [
    {
        'EXTENSIONS': ['jpg', 'jpeg', 'mov', 'mp4', 'm4v', '3gp'],
        'PATH': '/data/photos',
    },
    {
        'EXTENSIONS': ['cr2'],
        'PATH': '/data/raw-photos',
    },
]
PHOTO_RAW_PROCESSED_DIR = '/data/raw-photos-processed'

MODEL_INFO_URL = 'https://photonix.org/models.json'

GRAPHENE = {
    'SCHEMA': 'photonix.web.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

APPEND_SLASHES = False

CORS_ORIGIN_WHITELIST = []
