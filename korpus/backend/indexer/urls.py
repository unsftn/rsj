# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
import indexer.search as old_search
import indexer.search_rustengine as new_search

app_name = 'индексирање'

urlpatterns = [
    path('reci/', new_search.search_rec),
    path('sufiks/', new_search.search_rec_sufiks),
    path('publikacije/', new_search.search_pub),
    path('oblici/', new_search.search_oblik_in_pub),
    path('naslovi/', new_search.search_naslov),
    path('duplikati/', new_search.check_dupes),
]

urlpatterns = format_suffix_patterns(urlpatterns)
