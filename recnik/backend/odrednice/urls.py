from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *
from .korpus_api import api_korpus

app_name = 'одреднице'

urlpatterns = [
    path('podvrsta-reci/', PodvrstaReciList.as_view(), name='podvrsta-reci-list'),
    path('podvrsta-reci/<int:pk>/', PodvrstaReciDetail.as_view(), name='podvrsta-reci-detail'),
    path('antonim/', AntonimList.as_view(), name='antonim-list'),
    path('antonim/<int:pk>/', AntonimDetail.as_view(), name='antonim-detail'),
    path('sinonim/', SinonimList.as_view(), name='sinonim-list'),
    path('sinonim/<int:pk>/', SinonimDetail.as_view(), name='sinonim-detail'),
    path('kolokacija/', KolokacijaList.as_view(), name='kolokacija-list'),
    path('kolokacija/<int:pk>/', KolokacijaDetail.as_view(), name='kolokacija-detail'),
    path('rec-u-kolokaciji/', RecUKolokacijiList.as_view(), name='rec-u-kolokaciji-list'),
    path('rec-u-kolokaciji/<int:pk>/', RecUKolokacijiDetail.as_view(), name='rec-u-kolokaciji-detail'),
    path('znacenje/', ZnacenjeList.as_view(), name='znacenje-list'),
    path('znacenje/<int:pk>/', ZnacenjeDetail.as_view(), name='znacenje-detail'),
    path('podznacenje/', PodznacenjeList.as_view(), name='podznacenje-list'),
    path('podznacenje/<int:pk>/', PodznacenjeDetail.as_view(), name='podznacenje-detail'),
    path('izraz-fraza/', IzrazFrazaList.as_view(), name='izrazfraza-list'),
    path('izraz-fraza/<int:pk>/', IzrazFrazaDetail.as_view(), name='izrazfraza-detail'),
    path('kvalifikator/', KvalifikatorList.as_view(), name='kvalifikator-list'),
    path('kvalifikator/<int:pk>/', KvalifikatorDetail.as_view(), name='kvalifikator-detail'),
    path('kvalifikator-odrednice/', KvalifikatorOdredniceList.as_view(), name='kvalifikator-odrednice-list'),
    path('kvalifikator-odrednice/<int:pk>/', KvalifikatorOdredniceDetail.as_view(), name='kvalifikator-odrednice-detail'),
    path('kvalifikator-znacenja/', KvalifikatorZnacenjaList.as_view(), name='kvalifikator-znacenja-list'),
    path('kvalifikator-znacenja/<int:pk>/', KvalifikatorZnacenjaDetail.as_view(), name='kvalifikator-znacenja-detail'),
    path('kvalifikator-podznacenja/', KvalifikatorPodznacenjaList.as_view(), name='kvalifikator-podznacenja-list'),
    path('kvalifikator-podznacenja/<int:pk>/', KvalifikatorPodznacenjaDetail.as_view(), name='kvalifikator-podznacenja-detail'),
    path('izmena-odrednice/', IzmenaOdredniceList.as_view(), name='izmena-odrednice-list'),
    path('izmena-odrednice/<int:pk>/', IzmenaOdredniceDetail.as_view(), name='izmena-odrednice-detail'),
    path('status-odrednice/', StatusList.as_view(), name='status-odrednice-list'),
    path('status-odrednice/<int:pk>/', StatusDetail.as_view(), name='status-odrednice-detail'),
    path('odrednica/', OdrednicaList.as_view(), name='odrednica-list'),
    path('odrednica/<int:pk>/', OdrednicaDetail.as_view(), name='odrednica-detail'),
    path('odrednica-latest/', OdrednicaLatestList.as_view(), name='odrednica-latest-list'),
    path('odrednica-changed/', OdrednicaLatestList.as_view(), name='odrednica-changed-list'),
    path('odrednica-popular/', OdrednicaPopularList.as_view(), name='odrednica-popular-list'),
    path('short-odrednica/', ShortOdrednicaList.as_view(), name='short-odrednica-list'),
    path('short-odrednica/<int:pk>/', ShortOdrednicaDetail.as_view(), name='short-odrednica-detail'),
    path('short-odrednica-alpha/', ShortOdrednicaListAlpha.as_view(), name='short-odrednica-list-alpha'),
    path('short-odrednica-with-notes/', ShortOdrednicaListWithNotes.as_view(), name='short-odrednica-list-with-notes'),
    path('save/', api_save_odrednica),
    path('delete/<int:odrednica_id>/', api_delete_odrednica),
    path('workflow/za-obradjivaca/<int:odrednica_id>/', api_predaj_obradjivacu),
    path('workflow/za-redaktora/<int:odrednica_id>/', api_predaj_redaktoru),
    path('workflow/za-urednika/<int:odrednica_id>/', api_predaj_uredniku),
    path('workflow/kraj/<int:odrednica_id>/', api_zavrsi_obradu),
    path('workflow/zaduzenja/<int:odrednica_id>/', api_change_roles),
    path('workflow/moje-odrednice/<int:page_size>/', api_moje_odrednice),
    path('workflow/nicije-odrednice/<int:page_size>/', api_nicije_odrednice),
    path('stats/obradjivaci/', api_statistika_obradjivaca),
    path('stats/grafikon/<int:tip_grafikona>/', api_grafikon),
    path('stats/odrednice-za-status/<int:status_id>/', api_odrednice_za_status),
    path('password/change/', change_password),
    path('password/forgot/', forgot_password),
    path('korisnici/', get_korisnici),
    path('korisnici/<int:id>/', get_korisnik),
    path('korisnici/obradjivaci/', get_obradjivaci),
    path('korisnici/redaktori/', get_redaktori),
    path('korisnici/urednici/', get_urednici),
    path('korisnici/administratori/', get_administratori),
    path('external/odrednica/<int:odrednica_id>/', api_korpus),
]

urlpatterns = format_suffix_patterns(urlpatterns)
