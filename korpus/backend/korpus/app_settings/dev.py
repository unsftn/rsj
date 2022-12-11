from .base import *

DEBUG = True
SECRET_KEY = 'x4f$k4b-21q!#6#2ovzx77_rsneenp2==3wa#fo#%so#p2w*0u'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'korpus',
        'USER': 'korpus',
        'PASSWORD': 'korpus',
        'HOST': 'localhost',
        'PORT': '3306',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    },
}

ELASTICSEARCH_HOST = 'http://localhost:9200'
RSJ_HOST = 'http://localhost:9201'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ADMINS = []
HEADER_COLOR_SCHEME = 'green'
