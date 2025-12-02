from .base import *
from .utils import read_or_get

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = read_or_get('/private/secrets', 'SECRET_KEY', '123456789012345678901234567890123456789')
DB_HOST = read_or_get('/private/secrets', 'DB_HOST', 'korpus-mysql')
ELASTICSEARCH_HOST = read_or_get('/private/secrets', 'ELASTICSEARCH_HOST', 'http://elastic-korpus:9200')
RSJ_HOST = read_or_get('/private/secrets', 'RSJ_HOST', 'http://elastic-recnik:9200')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'korpus',
        'USER': 'korpus',
        'PASSWORD': 'korpus',
        'HOST': DB_HOST,
        'PORT': '',
        'STORAGE_ENGINE': 'INNODB',
        'OPTIONS': {
            'charset': 'utf8mb4'
        }
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = read_or_get('/private/secrets', 'EMAIL_HOST', 'smtp.uns.ac.rs')
EMAIL_PORT = eval(read_or_get('/private/secrets', 'EMAIL_PORT', '587')) or 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = read_or_get('/private/secrets', 'EMAIL_HOST_USER', '******')
EMAIL_HOST_PASSWORD = read_or_get('/private/secrets', 'EMAIL_HOST_PASSWORD', '**********')
HEADER_COLOR_SCHEME = read_or_get('/private/secrets', 'HEADER_COLOR_SCHEME', 'green')
CSRF_TRUSTED_ORIGINS = ['https://*.rsj.rs']
ADMINS = [('Branko Milosavljevic', 'mbranko@uns.ac.rs')]
GSHEETS_TOKEN = read_or_get('/private/secrets', 'GSHEETS_TOKEN', '/app/gsheets-token.json')
GSHEETS_CREDENTIALS = read_or_get('/private/secrets', 'GSHEETS_CREDENTIALS', '/app/gsheets-credentials.json')
KORPUS_SPREADSHEET_ID = read_or_get('/private/secrets', 'KORPUS_SPREADSHEET_ID', '1tZkiNjtwA6smaM8xnYrCEK1UszibU4rUXEDS-jw4i6o')
KORPUS_API_TOKEN = read_or_get('/private/secrets', 'KORPUS_API_TOKEN', 'korpus')

# File upload settings - 10 MB limit
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
