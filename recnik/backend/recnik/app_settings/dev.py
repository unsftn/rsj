from .base import *

DEBUG = True
SECRET_KEY = 'x4f$k4b-21q!#6#2ovzx77_rsneenp2==3wa#fo#%so#p2w*0u'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recnik',
        'USER': 'recnik',
        'PASSWORD': 'recnik',
        'HOST': 'localhost',
        'PORT': '3306',
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

ELASTICSEARCH_HOST = 'http://localhost:9201'
KORPUS_HOST = 'http://localhost:9200'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
HEADER_COLOR_SCHEME = 'purple'
OBRADA_TUDJIH = True
KORPUS_API_TOKEN = 'korpus'
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://localhost:4200']
KORPUS_URL = 'http://localhost:8000'
