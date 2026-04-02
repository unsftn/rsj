# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
import pretraga.rest as old_rest
import pretraga.rest_rustengine as new_rest

app_name = 'претрага'

urlpatterns = [
    path('odrednica/', new_rest.odrednica),
    path('odrednica-znacenja/', new_rest.search_odrednica_sa_znacenjima),
    path('odrednica/duplicate/', new_rest.check_duplicate),
    path('naslov/<int:izvor_id>/', new_rest.load_opis_from_korpus_wrapped),
    path('naslov/', new_rest.search_opis_in_korpus)
]

urlpatterns = format_suffix_patterns(urlpatterns)
