
# ==============================================================================
# Imports
# ==============================================================================

import os
from config.env import env, BASE_DIR

env.read_env(os.path.join(BASE_DIR, ".env"))


# ==============================================================================
# Base Configuration
# ==============================================================================
SECRET_KEY = env("SECRET_KEY", default='=ug_ucl@yi6^mrcjyz%(u0%&g2adt#bz3@yos%#@*t#t!ypx=a')

DEBUG = env.bool("DEBUG", default=True)

ASGI_APPLICATION = "config.asgi.application"
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])



# ==============================================================================
# Django Applications
# ==============================================================================
LOCAL_APPS = [
    'online_shop.core.apps.CoreConfig',
    'online_shop.common.apps.CommonConfig',
    'online_shop.users.apps.UsersConfig',
    "online_shop.products",
    "online_shop.sms_gateway",
    "online_shop.transactions",
    "online_shop.payment_gateway",
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',
    'drf_spectacular',
    'django_extensions',
    "drf_error_handler",
    "django_elasticsearch_dsl",
    "channels",
]

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

# ==============================================================================
# Middleware
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "online_shop.api.middleware.RequestLoggingMiddleware",
]

# ==============================================================================
# URL Configuration
# ==============================================================================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


# ==============================================================================
# Templates
# ==============================================================================

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

# ==============================================================================
# Database
# ==============================================================================

DATABASES = {
    'default': env.db('DATABASE_URL', default='psql://parham:paripari85@127.0.0.1:5432/online_shop'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': 'parham',
            'PASSWORD': 'paripari85',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

# ==============================================================================
# Authentication
# ==============================================================================


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
AUTH_USER_MODEL = 'users.BaseUserModel'



STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ==============================================================================
# Django REST Framework
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_RENDERER_CLASSES": [
        "online_shop.api.renderer.CustomResponseRenderer",
    ],
    'EXCEPTION_HANDLER': "drf_error_handler.handler.exception_handler",
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# ==============================================================================
# Redis Cache
# ==============================================================================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}
CACHE_TTL = 60 * 15


APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'online_shop.users.validators.NumberValidator'},
    {'NAME': 'online_shop.users.validators.LetterValidator'},
    {'NAME': 'online_shop.users.validators.SpecialCharValidator'},
]


# ==============================================================================
# Logging
# ==============================================================================
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
os.makedirs(BASE_DIR / "logs", exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {module}:{lineno} - {message}",
            "style": "{",
        },
    },

    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "when": "midnight",      
            "interval": 1,           
            "backupCount": 30,       
            "encoding": "utf-8",
            "formatter": "verbose",
        },

        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },

    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


# ==============================================================================
# DRF Error Handler
# ==============================================================================
DRF_ERROR_HANDLER = {
    "VALIDATION_ERROR_BUSINESS_STATUS_CODE": 1001,
    "PARSE_ERROR_BUSINESS_STATUS_CODE": 1002,
    "AUTHENTICATION_FAILED_BUSINESS_STATUS_CODE": 1003,
    "NOT_AUTHENTICATION_BUSINESS_STATUS_CODE": 1004,
    "PERMISSION_DENIED_BUSINESS_STATUS_CODE": 1005,
    "NOT_FOUND_BUSINESS_STATUS_CODE": 1006,
    "METHOD_NOT_ALLOWED_BUSINESS_STATUS_CODE": 1007,
    "NOT_ACCEPTABLE_BUSINESS_STATUS_CODE": 1008,
    "UNSUPPORTED_MEDIA_TYPE_BUSINESS_STATUS_CODE": 1009,
    "THROTTLED_BUSINESS_STATUS_CODE": 1010,
    "EXCEPTION_FORMATTER_CLASS": "online_shop.utils.formatters.StatusExceptionFormatter",
}


# ==============================================================================
# WebSocket (Channels)
# ==============================================================================

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                ("127.0.0.1", 6379),
            ],
        },
    },
}


# ==============================================================================
# External Services
# ==============================================================================

from config.settings.kavenegar import *
from config.settings.elastic import *
from config.settings.zarinpal import *
from config.settings.cors import *  # noqa
from config.settings.jwt import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.swagger import *  # noqa
from config.settings.unfold import *