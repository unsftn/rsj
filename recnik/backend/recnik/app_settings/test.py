from .base import *

DEBUG = True
SECRET_KEY = 'x4f$k4b-21q!#6#2ovzx77_rsneenp2==3wa#fo#%so#p2w*0u'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db'
    }
}
