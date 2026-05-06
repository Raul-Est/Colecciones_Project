import os

from .base import *  # noqa: F401, F403, F405

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-dev-key-cambiar-en-produccion'
)

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
