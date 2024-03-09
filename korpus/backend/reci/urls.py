from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'речи'

urlpatterns = [
    path('imenice/', ImenicaList.as_view()),
    path('imenice/<int:pk>/', ImenicaDetail.as_view()),
    path('glagoli/', GlagolList.as_view()),
    path('glagoli/<int:pk>/', GlagolDetail.as_view()),
    path('pridevi/', PridevList.as_view()),
    path('pridevi/<int:pk>/', PridevDetail.as_view()),
    path('predlozi/', PredlogList.as_view()),
    path('predlozi/<int:pk>/', PredlogDetail.as_view()),
    path('recce/', ReccaList.as_view()),
    path('recce/<int:pk>/', ReccaDetail.as_view()),
    path('uzvici/', UzvikList.as_view()),
    path('uzvici/<int:pk>/', UzvikDetail.as_view()),
    path('veznici/', VeznikList.as_view()),
    path('veznici/<int:pk>/', VeznikDetail.as_view()),
    path('zamenice/', ZamenicaList.as_view()),
    path('zamenice/<int:pk>/', ZamenicaDetail.as_view()),
    path('brojevi/', BrojList.as_view()),
    path('brojevi/<int:pk>/', BrojDetail.as_view()),
    path('prilozi/', PrilogList.as_view()),
    path('prilozi/<int:pk>/', PrilogDetail.as_view()),

    path('save/imenica/', save_imenica),
    path('save/glagol/', save_glagol),
    path('save/pridev/', save_pridev),
    path('save/predlog/', save_predlog),
    path('save/recca/', save_recca),
    path('save/uzvik/', save_uzvik),
    path('save/veznik/', save_veznik),
    path('save/zamenica/', save_zamenica),
    path('save/broj/', save_broj),
    path('save/prilog/', save_prilog),

    path('password/change/', change_password),
    path('password/forgot/', forgot_password),
    path('user/<int:user_id>/', user_info),

    # path('stats/bur/', get_broj_reci_za_korisnika),
    # path('stats/bur/svi/', get_broj_reci_za_sve),
    path('stats/unos-reci/', get_statistika_unosa_reci),
    path('stats/moje-reci/', moje_reci),
    path('stats/reci-korisnika/<int:user_id>/', reci_korisnika),
    path('stats/broj-mojih-reci/', broj_mojih_reci),

    path('delete/<int:word_type>/<int:word_id>/', delete_word),
]

urlpatterns = format_suffix_patterns(urlpatterns)
