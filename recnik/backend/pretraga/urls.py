# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'претрага'

urlpatterns = [
    path('odrednica/', odrednica),
    path('odrednica/duplicate/', check_duplicate),
    path('naslov/<int:izvor_id>/', load_opis_from_korpus),
    path('naslov/', search_opis_in_korpus),
]

urlpatterns = format_suffix_patterns(urlpatterns)
