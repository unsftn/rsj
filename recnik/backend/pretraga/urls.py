# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'претрага'

urlpatterns = [
    path('odrednica/', odrednica),
    path('odrednica-znacenja/', search_odrednica_sa_znacenjima),
    path('odrednica/duplicate/', check_duplicate),
    path('naslov/<int:izvor_id>/', load_opis_from_korpus_wrapped),
    path('naslov/', search_opis_in_korpus),
]

urlpatterns = format_suffix_patterns(urlpatterns)
