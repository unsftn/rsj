from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'recnikproxy'

urlpatterns = [
    path('search/', search),
    path('read/<int:odrednica_id>/', read),
    path('save/', save),
]

urlpatterns = format_suffix_patterns(urlpatterns)
