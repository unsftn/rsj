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
    path('filter-publikacije/', FilterPublikacijeList.as_view()),
    path('filter-publikacije/<int:pk>/', FilterPublikacijeDetail.as_view()),
    path('parametar-filtera/', ParametarFilteraList.as_view()),
    path('parametar-filtera/<int:pk>/', ParametarFilteraDetail.as_view()),
    path('save/publikacija/', api_create_publication),
    path('save/pubfile/<int:pub_id>/', api_add_files_to_pub),
    path('save/text/', api_create_text),
    path('save/filters/<int:pub_id>/', api_set_filters),
    path('delete/pubfile/<int:pub_id>/', api_remove_files_from_pub),
    path('reorder/pubfile/<int:pub_id>/', api_reorder_files),
    path('delete/text/<int:pub_id>/', api_delete_texts_for_pub),
    path('extract/<int:pub_id>/', api_extract_text_for_pub),
    path('svi-filteri/', api_filter_list),
    path('primeni-filtere/<int:pub_id>/', api_apply_filters),
]

urlpatterns = format_suffix_patterns(urlpatterns)
