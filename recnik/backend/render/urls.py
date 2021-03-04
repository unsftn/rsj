from django.urls import path
from .rest import *

app_name = 'render'

urlpatterns = [
    path('odrednice/latest/<int:page_size>/', odrednice_latest),
    path('odrednice/newest/<int:page_size>/', odrednice_newest),
    path('odrednice/popular/<int:page_size>/', odrednice_popular),
    path('preview/', api_preview_odrednica),
    path('tip-dokumenta/', TipRenderovanogDokumentaList.as_view(), name='tip-renderovanog-dokumenta-list'),
    path('tip-dokumenta/<int:pk>/', TipRenderovanogDokumentaDetail.as_view(), name='tip-renderovanog-dokumenta-detail'),
    path('dokument/', RenderovaniDokumentList.as_view(), name='renderovani-dokument-list'),
    path('dokument/<int:pk>/', RenderovaniDokumentDetail.as_view(), name='renderovani-dokument-detail'),
]
