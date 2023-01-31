from datetime import datetime, timedelta
import json
import logging
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.db.models import Q
from django.db.models.functions import Collate
from django.template.loader import get_template
from django.utils import timezone
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
        if rec.prvo_slovo.lower() in AZBUKA:
            letter_cache[rec.prvo_slovo.upper()].append(rec)
    slova = [{'slovo': k.upper(), 'reci': letter_cache[k.upper()]} for k in AZBUKA if len(letter_cache[k.upper()]) > 0]
    return slova


def sledece_slovo(tekst, pos=None):
    if pos is None:
        pos = len(tekst) - 1
    if tekst[pos] == 'ш':
        tekst = tekst[:pos] # + 'а' + tekst[pos+1:]
        return sledece_slovo(tekst, pos-1)
    else:
        try:
            index = AZBUKA.index(tekst[pos].lower())
        except ValueError:
            log.warn(f'Neispravno slovo: {tekst[pos].lower()}')
            return tekst
        return tekst[:pos] + AZBUKA[index+1] + tekst[pos+1:]


def dodaj_opseg_slova(opseg, queryset):
    if not opseg:
        return queryset
    result = Q()
    delovi = [x.strip().lower() for x in opseg.split(',') if x.strip()]
    for deo in delovi:
        if '-' in deo:
            oddo = deo.split('-')
            if len(oddo) != 2:
                continue
            part = Q(tekst__gte=oddo[0], tekst__lte=sledece_slovo(oddo[1]))
        else:
            part = Q(tekst__startswith=deo)
        result = result | part
    queryset = queryset.filter(result)
    return queryset


def ima_korpus_nema_recnik():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=True, prvo_slovo__in=AZBUKA).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'upit': None,
        'filename': f'ima_srpko_nema_rsj.pdf',
        'naslov': 'Речи којих нема у Једнотомнику а има у корпусу',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def ima_korpus_nema_recnik_f_vece_10():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=True, prvo_slovo__in=AZBUKA, broj_pojavljivanja__gt=10).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'upit': None,
        'filename': f'ima_srpko_nema_rsj_f_vece_10.pdf',
        'naslov': 'Речи којих нема у Једнотомнику а има у корпусу са F>10',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def ima_korpus_nema_recnik_f_manje_10():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=True, prvo_slovo__in=AZBUKA, broj_pojavljivanja__lte=10).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'upit': None,
        'filename': f'ima_srpko_nema_rsj_f_manje_10.pdf',
        'naslov': 'Речи којих нема у Једнотомнику а има у корпусу са F<=10',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def ima_korpus_ima_recnik_f_vece_10():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=False, prvo_slovo__in=AZBUKA, broj_pojavljivanja__gt=10).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'upit': None,
        'filename': f'ima_srpko_ima_rsj_f_vece_10.pdf',
        'naslov': 'Речи којих има у Једнотомнику и у корпусу са F>10',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def ima_korpus_ima_recnik_f_manje_10():
    reci = RecZaOdluku.objects.filter(
        recnik_id__isnull=True, prvo_slovo__in=AZBUKA, broj_pojavljivanja__lte=10).order_by(
            Collate('tekst', 'utf8mb4_croatian_ci'))
    return {
        'upit': None,
        'filename': f'ima_srpko_ima_rsj_f_manje_10.pdf',
        'naslov': 'Речи којих има у Једнотомнику и у корпусу са F<=10',
        'datum': sada(),
        'slova': grupisi_po_slovima(reci)
    }


def dinamicki(upit, rbr):
    reci = RecZaOdluku.objects.all()
    if upit['u_recniku'] is not None:
        reci = reci.filter(recnik_id__isnull=not upit['u_recniku'])
    if upit['u_korpusu'] is not None:
        reci = reci.filter(korpus_id__isnull=not upit['u_korpusu'])
    if upit['frek_od'] is not None:
        reci = reci.filter(broj_pojavljivanja__gte=upit['frek_od'])
    if upit['frek_do'] is not None:
        reci = reci.filter(broj_pojavljivanja__lte=upit['frek_do'])
    if len(upit['odluke']) > 0:
        reci = reci.filter(odluka__in=upit['odluke'])
    if len(upit['opseg_slova']) > 0:
        reci = dodaj_opseg_slova(upit['opseg_slova'], reci)
    reci = reci.order_by(Collate('tekst', 'utf8mb4_croatian_ci'))
    upit['odluke'] = [ODLUKE[x-1][1] for x in upit['odluke']]
    return {
        'upit': upit,
        'filename': f'izvestaj-{rbr}.pdf',
        'naslov': 'Динамички извештај',
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
    start_time = timezone.now()
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
    end_time = timezone.now()
    log.info(f'Generisanje izvestaja {filename} trajalo {end_time-start_time}')


def dinamicki_izvestaj_task(task_id):
    try:
        dinizv = DinamickiIzvestaj.objects.get(id=task_id)
        upit = json.loads(dinizv.upit)
        dinizv.vreme_pocetka = timezone.now()
        dinizv.save()
        ctx = dinamicki(upit, dinizv.id)
        izvestaj(ctx)
        dinizv.zavrsen = True
        dinizv.vreme_zavrsetka = timezone.now()
        dinizv.save()

        # obrisi izvestaje starije od 30 dana
        stariji_od_30_dana = timezone.now() - timedelta(days=30)
        for di in DinamickiIzvestaj.objects.filter(vreme_zahteva__lte=stariji_od_30_dana):
            filename = os.path.join(settings.MEDIA_ROOT, 'izvestaji', f'izvestaj-{di.id}.pdf')
            os.remove(filename)
    except DinamickiIzvestaj.DoesNotExist:
        log.fatal(f'Dinamicki izvestaj {task_id} nije pronadjen')


def generisi_predefinisane():
    ctx = ima_korpus_nema_recnik()
    izvestaj(ctx)
    ctx = ima_korpus_nema_recnik_f_vece_10()
    izvestaj(ctx)
    ctx = ima_korpus_nema_recnik_f_manje_10()
    izvestaj(ctx)
    ctx = ima_korpus_ima_recnik_f_vece_10()
    izvestaj(ctx)
    ctx = ima_korpus_ima_recnik_f_manje_10()
    izvestaj(ctx)
