from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .indexer import search
from .rest import *

app_name = 'речи'

urlpatterns = [
    path('pretraga/', search, name='search'),
    path('imenice/', ImenicaList.as_view(), name='imenica-list'),
    path('imenice/<int:pk>/', ImenicaDetail.as_view(), name='imenica-detail'),
    path('glagoli/', GlagolList.as_view(), name='glagol-list'),
    path('glagoli/<int:pk>/', GlagolDetail.as_view(), name='glagol-detail'),
    path('pridevi/', PridevList.as_view(), name='pridev-list'),
    path('pridevi/<int:pk>/', PridevDetail.as_view(), name='pridev-detail'),
    path('save/imenica/', save_imenica, name='save-imenica'),
    path('save/glagol/', save_glagol, name='save-glagol'),
    path('save/pridev/', save_pridev, name='save-pridev'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
