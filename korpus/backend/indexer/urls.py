# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .search import *

app_name = 'индексирање'

urlpatterns = [
    path('reci/', search_rec),
    path('publikacije/', search_pub),
]

urlpatterns = format_suffix_patterns(urlpatterns)
