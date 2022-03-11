# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'публикације'

urlpatterns = [
    path('vrsta-publikacije/', VrstaPublikacijeList.as_view()),
    path('vrsta-publikacije/<int:pk>/', VrstaPublikacijeDetail.as_view()),
    path('potkorpus/', PotkorpusList.as_view()),
    path('potkorpus/<int:pk>/', PotkorpusDetail.as_view()),
    path('publikacija/', PublikacijaList.as_view()),
    path('publikacija/<int:pk>/', PublikacijaDetail.as_view()),
    path('publikacija/<int:pid>/tekst/<int:fid>/', api_tekst),
    path('autor/', AutorList.as_view()),
    path('autor/<int:pk>/', AutorDetail.as_view()),
    path('tekst-publikacije/', TekstPublikacijeList.as_view()),
    path('tekst-publikacije/<int:pk>/', TekstPublikacijeDetail.as_view()),
    path('fajl-publikacije/', FajlPublikacijeList.as_view()),
    path('fajl-publikacije/<int:pk>/', FajlPublikacijeDetail.as_view()),
    path('save/publikacija/', api_create_publication),
    path('save/pubfile/<int:pub_id>/', api_add_files_to_pub),
    path('save/text/', api_create_text),
    path('delete/pubfile/<int:pub_id>/', api_remove_files_from_pub),
    path('reorder/pubfile/<int:pub_id>/', api_reorder_files),
]

urlpatterns = format_suffix_patterns(urlpatterns)
