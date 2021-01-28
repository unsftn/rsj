# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'претрага'

urlpatterns = [
    path('odrednice/', odrednica),
    path('korpus/', korpus),
]

urlpatterns = format_suffix_patterns(urlpatterns)
