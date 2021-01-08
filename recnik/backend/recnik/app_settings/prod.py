from .base import *
from .utils import read_or_get
import os

DEBUG = False
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recnik',
        'USER': 'recnik',
        'PASSWORD': 'recnik',
        'HOST': 'recnik-mysql',
        'PORT': '',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    }
}
SECRET_KEY = read_or_get('/private/secrets', 'SECRET_KEY', None)
