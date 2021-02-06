import logging
import string
import tempfile
from django.core.files import File
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration
from odrednice.serializers import CreateOdrednicaSerializer
from odrednice.models import *
from .models import *

log = logging.getLogger(__name__)
AZBUKA = 'абвгдђежзијклљмнњопрстћуфхцчџш'
ROD = {1: 'м', 2: 'ж', 3: 'с'}
GVID = {1: 'свр.', 2: 'несвр.', 3: 'двовид.'}


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def tacka(tekst):
    if len(tekst) < 1:
        return tekst
    if tekst[-1] not in string.punctuation:
        return tekst + '.'
    return tekst


def font_fetcher(url):
    print(url)
    if url.startswith('fonts/'):
        font_path = finders.find(url)
        print(f'loading font: {font_path}')
        font_file = open(font_path, 'r')
        return {'file_obj': font_file}
    return default_url_fetcher(url)


def render_izrazi_fraze(izrazifraze):
    tekst = ''
    for izfr in izrazifraze:
        tekst += f' &#8212; <i>{tacka(izfr.opis)}</i>'
    return tekst


def render_kvalifikatori(kvalifikatori):
    tekst = ''
    for kvod in kvalifikatori:
        tekst += f' <small>{tacka(kvod.kvalifikator.skracenica)}</small> '
    return tekst


def render_podznacenje(podznacenje):
    tekst = ''
    tekst += render_kvalifikatori(podznacenje.kvalifikatorpodznacenja_set.all().order_by('redni_broj'))
    tekst += f'{tacka(podznacenje.tekst)}'
    tekst += render_izrazi_fraze(podznacenje.izrazfraza_set.all().order_by('redni_broj'))
    return tekst


def render_znacenje(znacenje):
    tekst = ''
    tekst += render_kvalifikatori(znacenje.kvalifikatorznacenja_set.all().order_by('redni_broj'))
    if znacenje.podznacenje_set.count() > 0:
        for rbr, podznacenje in enumerate(znacenje.podznacenje_set.all().order_by('redni_broj')):
            tekst += f' <b>{AZBUKA[rbr]}.</b> ' + render_podznacenje(podznacenje)
        return tekst
    else:
        tekst += f'{tacka(znacenje.tekst)}'
        tekst += render_izrazi_fraze(znacenje.izrazfraza_set.all().order_by('redni_broj'))
        return tekst


def render_one(odrednica):
    html = f'<b>{odrednica.rec}</b>'
    if odrednica.varijantaodrednice_set.count() > 0:
        html += f' ({", ".join([vod.tekst for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj")])})'
    if odrednica.vrsta == 0:  # imenica
        # if ima nastavak, dodaj nastavak
        html += f' <small>{ROD[odrednica.rod]}</small> '
    if odrednica.vrsta == 1:  # glagol
        if odrednica.nastavak:
            html += f', {odrednica.nastavak} '
        if odrednica.prezent:
            html += f', {odrednica.prezent} '
        if odrednica.glagolski_vid > 0:
            html += f'<small>{GVID[odrednica.glagolski_vid]}</small> '
    if odrednica.vrsta == 2:  # pridev
        if odrednica.nastavak:
            html += f', {odrednica.nastavak} '
    if odrednica.vrsta == 3:
        html += f' <small>прил.</small> '
    if odrednica.vrsta == 6:
        html += f' <small>узв.</small> '
    if odrednica.vrsta == 7:
        html += f' <small>речца</small> '
    if odrednica.vrsta == 8:
        html += f' <small>везн.</small> '
    if odrednica.znacenje_set.count() == 1:
        html += render_znacenje(odrednica.znacenje_set.first())
    else:
        for rbr, znacenje in enumerate(odrednica.znacenje_set.all(), start=1):
            html += f' <b>{rbr}.</b> ' + render_znacenje(znacenje)
    html = tacka(html)
    return mark_safe(html)


def render_one_div(odrednica, css_class='odrednica'):
    return mark_safe(f'<div class="{css_class}" data-id="{odrednica.id}">{render_one(odrednica)}</div>')


def render_many(odrednice, css_class='odrednica'):
    return mark_safe(''.join([render_one_div(od, css_class) for od in odrednice]))


def render_slovo(odrednice, slovo):
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=1)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal('Nije pronadjen tip renderovanog dokumenta: id=1')
        return None
    template = get_template('render/odrednice.html')
    rendered_odrednice = [render_one(o) for o in odrednice]
    context = {'odrednice': rendered_odrednice, 'slovo': slovo.upper()}
    html_text = template.render(context)
    html = HTML(string=html_text, url_fetcher=font_fetcher)
    css_file_name = finders.find('print-styles/slovo.css')
    with open(css_file_name, 'r') as css_file:
        css_text = css_file.read()
    font_config = FontConfiguration()
    css = CSS(string=css_text, font_config=font_config, url_fetcher=font_fetcher)
    temp_file = tempfile.TemporaryFile()
    html.write_pdf(temp_file, stylesheets=[css], font_config=font_config)
    novi_dokument = RenderovaniDokument()
    novi_dokument.tip_dokumenta = trd
    novi_dokument.vreme_rendera = now()
    novi_dokument.save()
    django_file = File(temp_file)
    novi_dokument.rendered_file.save(get_rendered_file_path(novi_dokument, None), django_file, True)
    return novi_dokument.rendered_file.name
