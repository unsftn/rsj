# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .search import *

app_name = 'индексирање'

urlpatterns = [
    path('reci/', search_rec),
    path('sufiks/', search_rec_sufiks),
    path('publikacije/', search_pub),
    path('oblici/', search_oblik_in_pub),
    path('naslovi/', search_naslov),
    path('duplikati/', check_dupes),
]

urlpatterns = format_suffix_patterns(urlpatterns)
