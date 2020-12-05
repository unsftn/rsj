from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'публикације'

urlpatterns = [
    path('vrsta-publikacije/', VrstaPublikacijeList.as_view()),
    path('vrsta-publikacije/<int:pk>/', VrstaPublikacijeDetail.as_view()),
    path('publikacija/', PublikacijaList.as_view()),
    path('publikacija/<int:pk>/', PublikacijaDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
