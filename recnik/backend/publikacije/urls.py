# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'публикације'

urlpatterns = [
    path('vrsta-publikacije/', VrstaPublikacijeList.as_view()),
    path('vrsta-publikacije/<int:pk>/', VrstaPublikacijeDetail.as_view()),
    path('publikacija/', PublikacijaList.as_view()),
    path('publikacija/<int:pk>/', PublikacijaDetail.as_view()),
    path('autor/', AutorList.as_view()),
    path('autor/<int:pk>/', AutorDetail.as_view()),
    path('tekst-publikacije/', TekstPublikacijeList.as_view()),
    path('tekst-publikacije/<int:pk>/', TekstPublikacijeDetail.as_view()),
    path('fajl-publikacije/', FajlPublikacijeList.as_view()),
    path('fajl-publikacije/<int:pk>/', FajlPublikacijeDetail.as_view()),
    path('create-publikacija/', api_create_publication),
    path('create-text/', api_create_text),
]

urlpatterns = format_suffix_patterns(urlpatterns)
