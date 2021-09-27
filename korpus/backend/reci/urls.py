from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'речи'

urlpatterns = [
    path('imenice/', ImenicaList.as_view(), name='imenica-list'),
    path('imenice/<int:pk>/', ImenicaDetail.as_view(), name='imenica-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
