from .base import *
from .utils import read_or_get
import os

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = read_or_get('/private/secrets', 'SECRET_KEY', '123456789012345678901234567890123456789')
DB_HOST = read_or_get('/private/secrets', 'DB_HOST', 'recnik-mysql')
ELASTICSEARCH_HOST = read_or_get('/private/secrets', 'ELASTICSEARCH_HOST', 'elastic-recnik')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recnik',
        'USER': 'recnik',
        'PASSWORD': 'recnik',
        'HOST': DB_HOST,
        'PORT': '',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    },
    'memory': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'file:memorydb?mode=memory&cache=shared',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.uns.ac.rs'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mbranko'
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = read_or_get('/private/secrets', 'EMAIL_HOST_PASSWORD', '**********')