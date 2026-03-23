# -*- coding: utf-8 -*-
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-temporary-key'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.51']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise',
    'tarefas.apps.TarefasConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projeto_saacb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # mantenha seus DIRS existentes
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # corrige W411
                'django.contrib.auth.context_processors.auth',  # corrige E402
                'django.contrib.messages.context_processors.messages',  # corrige E404
            ],
        },
    },
]

WSGI_APPLICATION = 'projeto_saacb.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data/db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / 'static']        # seus arquivos fonte ficam aqui
STATIC_ROOT = BASE_DIR / 'staticfiles'          # collectstatic grava aqui
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVER_EMAIL = 'root@localhost'

ADMINS = [('Admin', 'admin@saacb.local')]

MANAGERS = []

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_AGE = 86400

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = False

SESSION_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_DOMAIN = None

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = False

CSRF_COOKIE_AGE = 31449600

CSRF_COOKIE_SAMESITE = 'Lax'

SECURE_BROWSER_XSS_FILTER_V1 = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'

SECURE_SSL_REDIRECT = False

SECURE_HSTS_SECONDS = 0

SECURE_HSTS_INCLUDE_SUBDOMAINS = False

SECURE_HSTS_PRELOAD = False

# DEFAULT_EXCEPTION_REPORTER = 'django.views.debug.DebugView'  # Removido - incompatível com Django 4.0+

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
