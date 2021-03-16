import logging
import re
import tempfile
from django.core.files import File
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration
from docx import Document
from htmldocx import HtmlToDocx
from odrednice.models import *
from .models import *

log = logging.getLogger(__name__)
AZBUKA = 'абвгдђежзијклљмнњопрстћуфхцчџш'
ROD = {1: 'м', 2: 'ж', 3: 'с', 4: 'м и ж', 5: 'м и с', 6: 'ж и с'}
GVID = {1: 'свр.', 2: 'несвр.', 3: 'свр. и несвр.'}
SPECIAL_MARKS = ['аор.', 'пр.', ' р.', 'трп.', 'вок.', 'ген.', 'мн.', 'зб.', 'им.', 'инстр.', 'лок.', 'дат.', 'јек.', 'имп.']
REGEX_ITALIC = re.compile('#+(.+)#+')
REGEX_SMALL = re.compile('\\$+(.+)\\$+')


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


def process_hash(tekst, in_italic=False):
    if in_italic:
        return REGEX_ITALIC.sub('</i>\\1<i>', tekst)
    else:
        return REGEX_ITALIC.sub('<i>\\1</i>', tekst)


def process_dollar(tekst, in_italic=False):
    if in_italic:
        return REGEX_SMALL.sub('</i><small>\\1</small><i>', tekst)
    else:
        return REGEX_SMALL.sub('<small>\\1</small>', tekst)


def process_tags(tekst, in_italic=False):
    return process_dollar(process_hash(tekst, in_italic), in_italic)


def render_konkordanse(konkordanse):
    retval = ''
    for k in konkordanse:
        retval += f'<i>{tacka(process_tags(k.opis, True))}</i> '
        if k.publikacija:
            retval += f'{tacka(k.publikacija.skracenica)}'
    return tacka(retval)


def render_izrazi_fraze_znacenja(izrazifraze):
    tekst = ''
    for izfr in izrazifraze:
        tekst += f' &#8212; <i>{process_tags(tacka(izfr.opis), True)}</i>'
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
        tekst += f' <i>{process_tags(tacka(izfr.opis), True)}</i>'
    return tekst


def render_podznacenje(podznacenje):
    tekst = '' + render_kvalifikatori(podznacenje.kvalifikatorpodznacenja_set.all().order_by('redni_broj'))

    tekst += f'{process_tags(tacka(podznacenje.tekst))}'

    if podznacenje.konkordansa_set.count() > 0:
        tekst = dvotacka(tekst)
        tekst += render_konkordanse(podznacenje.konkordansa_set.all().order_by('redni_broj'))

    tekst += render_izrazi_fraze_znacenja(podznacenje.izrazfraza_set.all().order_by('redni_broj'))
    return tekst


def render_znacenje(znacenje):
    tekst = '' + render_kvalifikatori(znacenje.kvalifikatorznacenja_set.all().order_by('redni_broj'))

    tekst += f'{process_tags(tacka(znacenje.tekst))}'

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
    html = f'<b>{odrednica.rec}'
    if odrednica.vrsta == 1 and odrednica.opciono_se:
        html += f' (се)'
    if odrednica.rbr_homonima:
        html += f' <sup>{odrednica.rbr_homonima}</sup>'
    html += f'</b>'

    # imenica
    if odrednica.vrsta == 0:
        if odrednica.nastavak:
            html += f', {odrednica.nastavak} '
        if odrednica.ijekavski:
            html += f' <small>јек.</small> <b>{odrednica.ijekavski}</b>'
        if odrednica.nastavak_ij:
            if odrednica.ijekavski:
                html += f', {odrednica.nastavak_ij}'
            else:
                html += f', <small>јек.</small> {odrednica.nastavak_ij}'
        if odrednica.varijantaodrednice_set.count() > 0:
            html += ' и '
            html += f' {", ".join([render_varijanta(vod) for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj")])}'
        html += f' <small>{ROD[odrednica.rod]}</small> '  # 4 roda
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # glagol
    if odrednica.vrsta == 1:
        if odrednica.varijantaodrednice_set.count() > 0:
            html += f' ({", ".join([vod.tekst for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj")])})'
        if odrednica.prezent:
            html += f', {odrednica.prezent}'
        if odrednica.ijekavski:
            html += f', <small>јек.</small> <b>{odrednica.ijekavski}</b>'
        if odrednica.prezent_ij:
            if odrednica.ijekavski:
                html += f', {odrednica.prezent_ij}'
            else:
                html += f', <small>јек.</small> {odrednica.prezent_ij}'
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '
        if odrednica.glagolski_vid:
            html += f' <small>{GVID[odrednica.glagolski_vid]}</small> '

    # pridev
    if odrednica.vrsta == 2:
        if odrednica.nastavak:
            html += f', {odrednica.nastavak} '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # prilog
    if odrednica.vrsta == 3:
        html += f' <small>прил.</small> '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # predlog
    if odrednica.vrsta == 4:
        html += f' <small>предл.</small> '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # zamenica
    if odrednica.vrsta == 5:
        html += f' <small>предл.</small> '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # uzvik
    if odrednica.vrsta == 6:
        html += f' <small>узв.</small> '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # recca
    if odrednica.vrsta == 7:
        html += f' <small>речца</small> '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # veznik
    if odrednica.vrsta == 8:
        html += f' <small>везн.</small> '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # broj
    if odrednica.vrsta == 9:
        html += f' <small>број</small> '
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

    # ostalo
    if odrednica.vrsta == 10:
        if odrednica.info:
            html += f' {process_special_marks(odrednica.info)} '

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
    if url.startswith('fonts/'):
        font_path = finders.find(url)
        font_file = open(font_path, 'r')
        return {'file_obj': font_file}
    return default_url_fetcher(url)


def enumerate_odrednice(odrednice):
    prev = None
    for o in odrednice:
        curr = o
        if prev and prev.rec == curr.rec:
            if not hasattr(prev, 'rbr'):
                prev.rbr = 1
                curr.rbr = 2
            else:
                curr.rbr = prev.rbr + 1
        prev = o


def render_slovo(slovo, file_format='pdf'):
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=1)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal('Nije pronadjen tip renderovanog dokumenta: id=1')
        return
    odrednice = Odrednica.objects.filter(rec__startswith=slovo[0].lower()).order_by('rec', 'rbr_homonima')
    # enumerate_odrednice(odrednice)
    rendered_odrednice = [render_one(o) for o in odrednice]
    context = {'odrednice': rendered_odrednice, 'slovo': slovo.upper()}
    if file_format == 'pdf':
        return render_to_pdf(context, 'render/pdf/slovo.html', trd, opis=f'слово {slovo[0].upper()}')
    elif file_format == 'docx':
        return render_to_docx(context, 'render/docx/slovo.html', trd, opis=f'слово {slovo[0].upper()}')
    else:
        return None


def render_recnik(file_format='pdf'):
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=2)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal('Nije pronadjen tip renderovanog dokumenta: id=2')
        return
    slova = []
    for s in AZBUKA:
        odrednice = Odrednica.objects.filter(rec__startswith=s).order_by('rec', 'rbr_homonima')
        # enumerate_odrednice(odrednice)
        slova.append({
            'slovo': s.upper(),
            'odrednice': [render_one(o) for o in odrednice]
        })
    context = {'slova': slova}
    if file_format == 'pdf':
        return render_to_pdf(context, 'render/pdf/recnik.html', trd)
    elif file_format == 'docx':
        return render_to_docx(context, 'render/docx/recnik.html', trd)
    else:
        return None


def render_to_pdf(context, template, doc_type, opis=''):
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
    novi_dokument = add_file_to_django(doc_type, opis, temp_file, 'pdf')
    return novi_dokument.rendered_file.name


def render_to_docx(context, template, doc_type, opis=''):
    tpl = get_template(template)
    html_text = tpl.render(context)
    document = Document()
    style = document.styles['Normal']
    font = style.font
    font.name = 'Dijakritika'
    new_parser = HtmlToDocx()
    new_parser.add_html_to_document(html_text, document)
    temp_file = tempfile.TemporaryFile()
    document.save(temp_file)
    novi_dokument = add_file_to_django(doc_type, opis, temp_file, 'docx')
    return novi_dokument.rendered_file.name


def add_file_to_django(doc_type, opis, file_path, file_type):
    novi_dokument = RenderovaniDokument()
    novi_dokument.tip_dokumenta = doc_type
    novi_dokument.vreme_rendera = now()
    novi_dokument.opis = opis
    novi_dokument.file_type = 1 if file_type == 'pdf' else 2
    novi_dokument.save()
    django_file = File(file_path)
    novi_dokument.rendered_file.save(get_rendered_file_path(novi_dokument, None), django_file, True)
    return novi_dokument
