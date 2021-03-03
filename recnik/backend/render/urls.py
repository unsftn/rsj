from django.urls import path
from .rest import *

app_name = 'render'

urlpatterns = [
    path('odrednice/latest/<int:page_size>/', odrednice_latest),
    path('odrednice/newest/<int:page_size>/', odrednice_newest),
    path('odrednice/popular/<int:page_size>/', odrednice_popular),
    path('preview/', api_preview_odrednica),
]
