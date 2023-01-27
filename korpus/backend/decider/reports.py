from datetime import datetime
import logging
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.db.models.functions import Collate
from django.template.loader import get_template
from django.utils.timezone import now
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.text.fonts import FontConfiguration
from .models import *

AZBUKA = [
    'а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к', 'л', 'љ', 'м',
    'н', 'њ', 'о', 'п', 'р', 'с', 'т', 'ћ', 'у', 'ф', 'х', 'ц', 'ч', 'џ', 'ш',
]

log = logging.getLogger(__name__)


def sada():
    return datetime.now().strftime('%d.%m.%Y. %H:%M')


def grupisi_po_slovima(reci):
    letter_cache = {k.upper(): [] for k in AZBUKA}
    for rec in reci:
        letter_cache[rec.prvo_slovo.upper()].append(rec)
    slova = [{'slovo': k.upper(), 'reci': letter_cache[k.upper()]} for k in AZBUKA]
    return slova


def ima_korpus_nema_recnik():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=True, prvo_slovo__in=AZBUKA).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'filename': f'{datetime.now().strftime("%Y%m%d")}_ima_srpko_nema_rsj.pdf',
        'naslov': 'Речи којих нема у Једнотомнику а има у корпусу',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def ima_korpus_nema_recnik_f_vece_10():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=True, prvo_slovo__in=AZBUKA, broj_pojavljivanja__gt=10).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'filename': f'{datetime.now().strftime("%Y%m%d")}_ima_srpko_nema_rsj_f_vece_10.pdf',
        'naslov': 'Речи којих нема у Једнотомнику а има у корпусу са F>10',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def ima_korpus_nema_recnik_f_manje_10():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=True, prvo_slovo__in=AZBUKA, broj_pojavljivanja__lte=10).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'filename': f'{datetime.now().strftime("%Y%m%d")}_ima_srpko_nema_rsj_f_manje_10.pdf',
        'naslov': 'Речи којих нема у Једнотомнику а има у корпусу са F<=10',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def ima_korpus_ima_recnik_f_vece_10():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=False, prvo_slovo__in=AZBUKA, broj_pojavljivanja__gt=10).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'filename': f'{datetime.now().strftime("%Y%m%d")}_ima_srpko_ima_rsj_f_vece_10.pdf',
        'naslov': 'Речи којих има у Једнотомнику и у корпусу са F>10',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def ima_korpus_ima_recnik_f_manje_10():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=True, prvo_slovo__in=AZBUKA, broj_pojavljivanja__lte=10).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'filename': f'{datetime.now().strftime("%Y%m%d")}_ima_srpko_ima_rsj_f_manje_10.pdf',
        'naslov': 'Речи којих има у Једнотомнику и у корпусу са F<=10',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def font_fetcher(url):
    if url.startswith('fonts/'):
        font_path = finders.find(url)
        font_file = open(font_path, 'r')
        return {'file_obj': font_file}
    return default_url_fetcher(url)


def izvestaj(context):
    start_time = now()
    log.info(f'Generisem izvestaj: {context["naslov"]}')
    tpl = get_template('decider/izvestaj.html')
    html_text = tpl.render(context)
    html = HTML(string=html_text, url_fetcher=font_fetcher)
    css_file_name = finders.find('print-styles/izvestaj.css')
    with open(css_file_name, 'r') as css_file:
        css_text = css_file.read()
    font_config = FontConfiguration()
    css = CSS(string=css_text, font_config=font_config, url_fetcher=font_fetcher)
    dir = os.path.join(settings.MEDIA_ROOT, 'izvestaji')
    if not os.path.isdir(dir):
        os.makedirs(dir)
    filename = os.path.join(dir, context['filename'])
    html.write_pdf(filename, stylesheets=[css], font_config=font_config)
    end_time = now()
    log.info(f'Generisanje izvestaja {filename} trajalo {end_time-start_time}')
