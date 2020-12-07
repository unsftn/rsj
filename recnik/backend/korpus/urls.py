from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'корпус'

urlpatterns = [
    path('vrsta-imenice/', VrstaImeniceList.as_view()),
    path('vrsta-imenice/<int:pk>/', VrstaImeniceDetail.as_view()),
    path('imenica/', ImenicaList.as_view()),
    path('imenica/<int:pk>/', ImenicaDetail.as_view()),
    path('glagol/', GlagolList.as_view()),
    path('glagol/<int:pk>/', GlagolDetail.as_view()),
    path('pridev/', PridevList.as_view()),
    path('pridev/<int:pk>/', PridevDetail.as_view()),
    path('save-imenica/', api_save_imenica),
    path('save-glagol/', api_save_glagol),
    path('save-pridev/', api_save_pridev),
]

urlpatterns = format_suffix_patterns(urlpatterns)
