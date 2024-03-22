from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'recnikproxy'

urlpatterns = [
    path('search/', search),
    path('read/<int:pk>/', read),
    path('save/<int:pk>', save),
]

urlpatterns = format_suffix_patterns(urlpatterns)
