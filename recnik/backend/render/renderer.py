import logging
import string
import tempfile
from django.core.files import File
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration
from odrednice.models import *
from .models import *

log = logging.getLogger(__name__)
AZBUKA = 'абвгдђежзијклљмнњопрстћуфхцчџш'
ROD = {1: 'м', 2: 'ж', 3: 'с'}
GVID = {1: 'свр.', 2: 'несвр.', 3: 'свр. и несвр.'}
SPECIAL_MARKS = ['аор.', 'пр. пр.', 'пр.пр.', 'р.пр.', 'р. пр.', 'трп.']


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def dvotacka(tekst):
    if len(tekst) < 1:
        return tekst
    if tekst[-1] == '.':
        return tekst[:-1] + ': '
    return tekst + ': '


def tacka(tekst):
    if len(tekst) < 1:
        return tekst
    if tekst[-1] == '>' and tekst[-5] == '.':
        return tekst
    if tekst[-1] not in '!"#$%&\'(*+,-./:;<=?@[\\]^_`{|}~':  # izbaceno: >)
        return tekst + '.'
    return tekst


def process_special_marks(tekst):
    for mark in SPECIAL_MARKS:
        tekst = tekst.replace(mark, f'<small>{mark}</small>')
    return tekst


def render_konkordanse(konkordanse):
    return tacka(', '.join([f'<i>{k.opis}</i>' for k in konkordanse]))


def render_izrazi_fraze_znacenja(izrazifraze):
    tekst = ''
    for izfr in izrazifraze:
        tekst += f' &#8212; <i>{tacka(izfr.opis)}</i>' 
    return tekst


def render_kvalifikatori(kvalifikatori):
    tekst = ''
    for kvod in kvalifikatori:
        tekst += f' <small>{tacka(kvod.kvalifikator.skracenica)}</small> '
    return tekst


def render_izrazi_fraze_odrednice(izrazifraze):
    tekst = ''
    for izfr in izrazifraze:
        tekst += f' &bull; <small><b>{izfr.tekst}</b></small> '
        tekst += render_kvalifikatori(izfr.kvalifikatorfraze_set.all().order_by('redni_broj'))
        tekst += f' <i>{tacka(izfr.opis)}</i>'
    return tekst


def render_podznacenje(podznacenje):
    tekst = ''
    tekst += render_kvalifikatori(podznacenje.kvalifikatorpodznacenja_set.all().order_by('redni_broj'))

    tekst += f'{tacka(podznacenje.tekst)}'

    if podznacenje.konkordansa_set.count() > 0:
        tekst = dvotacka(tekst)
        tekst += render_konkordanse(podznacenje.konkordansa_set.all().order_by('redni_broj'))

    tekst += render_izrazi_fraze_znacenja(podznacenje.izrazfraza_set.all().order_by('redni_broj'))
    return tekst


def render_znacenje(znacenje):
    tekst = ''
    tekst += render_kvalifikatori(znacenje.kvalifikatorznacenja_set.all().order_by('redni_broj'))

    tekst += f'{tacka(znacenje.tekst)}'

    if znacenje.konkordansa_set.count() > 0:
        tekst = dvotacka(tekst)
        tekst += render_konkordanse(znacenje.konkordansa_set.all().order_by('redni_broj'))

    tekst += render_izrazi_fraze_znacenja(znacenje.izrazfraza_set.all().order_by('redni_broj'))

    if znacenje.podznacenje_set.count() > 0:
        for rbr, podznacenje in enumerate(znacenje.podznacenje_set.all().order_by('redni_broj')):
            tekst += f' <b>{AZBUKA[rbr]}.</b> ' + render_podznacenje(podznacenje)
    return tekst


def render_varijanta(var):
    return f'<b>{var.tekst}</b>' + ((', ' + var.nastavak) if var.nastavak else '')


def render_one(odrednica):
    if odrednica.vrsta == 1 and odrednica.opciono_se:
        html = f'<b>{odrednica.rec} (се)</b>'
    else:
        html = f'<b>{odrednica.rec}</b>'
    if odrednica.vrsta == 0:  # imenica
        if odrednica.nastavak:
            html += f', {odrednica.nastavak} '
        if odrednica.varijantaodrednice_set.count() > 0:
            html += ' и '
            html += f' {", ".join([render_varijanta(vod) for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj")])}'
        html += f' <small>{ROD[odrednica.rod]}</small> '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '
    if odrednica.vrsta == 1:  # glagol
        if odrednica.varijantaodrednice_set.count() > 0:
            html += f' ({", ".join([vod.tekst for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj")])})'
        if odrednica.prezent:
            html += f', {odrednica.prezent} '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '
        if odrednica.glagolski_vid:
            html += f'<small>{GVID[odrednica.glagolski_vid]}</small> '
    if odrednica.vrsta == 2:  # pridev
        if odrednica.nastavak:
            html += f', {odrednica.nastavak} '
        if odrednica.info:
            html += f' ({odrednica.info}) '
    if odrednica.vrsta == 3:
        html += f' <small>прил.</small> '
        if odrednica.info:
            html += f' ({odrednica.info}) '
    if odrednica.vrsta == 6:
        html += f' <small>узв.</small> '
        if odrednica.info:
            html += f' ({odrednica.info}) '
    if odrednica.vrsta == 7:
        html += f' <small>речца</small> '
        if odrednica.info:
            html += f' ({odrednica.info}) '
    if odrednica.vrsta == 8:
        html += f' <small>везн.</small> '
        if odrednica.info:
            html += f' ({odrednica.info}) '
    html += render_kvalifikatori(odrednica.kvalifikatorodrednice_set.all().order_by('redni_broj'))
    if odrednica.znacenje_set.count() == 1:
        html += render_znacenje(odrednica.znacenje_set.first())
    else:
        for rbr, znacenje in enumerate(odrednica.znacenje_set.filter(znacenje_se=False), start=1):
            html += f' <b>{rbr}.</b> ' + render_znacenje(znacenje)
        if odrednica.znacenje_set.filter(znacenje_se=True).count() > 0:
            html += f' <b>&#9632; ~ се</b> '
            for rbr, znacenje in enumerate(odrednica.znacenje_set.filter(znacenje_se=True), start=1):
                html += f' <b>{rbr}.</b> ' + render_znacenje(znacenje)
    html += render_izrazi_fraze_odrednice(odrednica.izrazfraza_set.all().order_by('redni_broj'))
    html = tacka(html)
    return mark_safe(html)


def render_one_div(odrednica, css_class='odrednica'):
    return mark_safe(f'<div class="{css_class}" data-id="{odrednica.id}">{render_one(odrednica)}</div>')


def render_many(odrednice, css_class='odrednica'):
    return mark_safe(''.join([render_one_div(od, css_class) for od in odrednice]))


def font_fetcher(url):
    log.info(url)
    if url.startswith('fonts/'):
        font_path = finders.find(url)
        log.info(font_path)
        font_file = open(font_path, 'r')
        return {'file_obj': font_file}
    return default_url_fetcher(url)


def render_slovo(slovo):
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=1)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal('Nije pronadjen tip renderovanog dokumenta: id=1')
        return
    odrednice = Odrednica.objects.filter(rec__startswith=slovo[0].lower()).order_by('rec')
    rendered_odrednice = [render_one(o) for o in odrednice]
    context = {'odrednice': rendered_odrednice, 'slovo': slovo.upper()}
    return render_to_file(context, 'render/slovo.html', trd, opis=f'слово {slovo[0].upper()}')


def render_recnik():
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=2)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal('Nije pronadjen tip renderovanog dokumenta: id=2')
        return
    slova = []
    for s in AZBUKA:
        slova.append({
            'slovo': s.upper(),
            'odrednice': [render_one(o) for o in Odrednica.objects.filter(rec__startswith=s).order_by('rec')]
        })
    context = {'slova': slova}
    log.info('TEST TEST')
    return render_to_file(context, 'render/recnik.html', trd)


def render_to_file(context, template, doc_type, opis=''):
    tpl = get_template(template)
    html_text = tpl.render(context)
    html_text = html_text.replace('&#9632;', '<small>&#9632;</small>')
    html = HTML(string=html_text, url_fetcher=font_fetcher)
    css_file_name = finders.find('print-styles/slovo.css')
    with open(css_file_name, 'r') as css_file:
        css_text = css_file.read()
    font_config = FontConfiguration()
    css = CSS(string=css_text, font_config=font_config, url_fetcher=font_fetcher)
    temp_file = tempfile.TemporaryFile()
    html.write_pdf(temp_file, stylesheets=[css], font_config=font_config)
    novi_dokument = RenderovaniDokument()
    novi_dokument.tip_dokumenta = doc_type
    novi_dokument.vreme_rendera = now()
    novi_dokument.opis = opis
    novi_dokument.save()
    django_file = File(temp_file)
    novi_dokument.rendered_file.save(get_rendered_file_path(novi_dokument, None), django_file, True)
    return novi_dokument.rendered_file.name
