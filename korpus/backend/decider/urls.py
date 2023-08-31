from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'одлуке'

urlpatterns = [
    path('generisani-spisak/', GenerisaniSpisakList.as_view()),
    path('generisani-spisak/poslednji/', poslednji_spisak),
    path('generisani-spisak/<int:pk>/', GenerisaniSpisakDetail.as_view()),
    path('rec-za-odluku/', RecZaOdlukuList.as_view()),
    path('rec-za-odluku-po/<str:slovo>/', RecZaOdlukuListFilteredPaged.as_view()),
    path('rec-za-odluku/<int:pk>/', RecZaOdlukuDetail.as_view()),
    path('report/', api_zahtev_za_izvestaj),
    path('report/<int:id>/', api_izvestaj),
    path('stats/broj-odluka/', api_broj_odluka),
]

urlpatterns = format_suffix_patterns(urlpatterns)
