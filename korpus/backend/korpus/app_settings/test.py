from .base import *

DEBUG = True
SECRET_KEY = 'x4f$k4b-21q!#6#2ovzx77_rsneenp2==3wa#fo#%so#p2w*0u'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db'
    },
}

ELASTICSEARCH_HOST = 'http://localhost:9200'
RSJ_HOST = 'http://localhost:9201'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

HEADER_COLOR_SCHEME = 'gray'
GSHEETS_TOKEN = 'gsheets-token.json'
GSHEETS_CREDENTIALS = 'gsheets-credentials.json'
KORPUS_SPREADSHEET_ID = '1tZkiNjtwA6smaM8xnYrCEK1UszibU4rUXEDS-jw4i6o'
