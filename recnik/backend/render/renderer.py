import logging
import re
import tempfile
from django.core.files import File
from django.contrib.staticfiles import finders
from django.db.models.functions import Collate
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
ROD = {1: 'м', 2: 'ж', 3: 'с', 4: 'м (ж)', 5: 'ж (м)', 6: 'м (с)', 7: 'с (м)', 8: 'ж (с)', 9: 'с (ж)'}
GVID = {1: 'свр.', 2: 'несвр.', 3: 'свр. и несвр.'}
SPECIAL_MARKS = ['ак.', 'аор.', 'безл.', 'бр.', 'везн.', 'вок.', 'ген.', 'гл.им.', 'дат.', 'зам.', 'зб.',
                 'изр.', 'имп.', 'импф.', 'инстр.', 'јд.', 'јек.', 'комп.', 'лок.', 'мн.', 'неодр.', 'непрел.',
                 'непром.', 'несвр.', 'ном.', 'одр.', 'оном.', 'повр.', 'пр.пр.', 'пр.сад.',
                 'предл.', 'през.', 'прел.', 'прил.', 'р.пр.', 'речца.', 'свр.', 'суп.', 'суп.мн.',
                 'трен.', 'трп.', 'трп.пр.', 'уз.повр.', 'узв.', 'уч.', 'арх.', 'гл.', 'гл.им.',
                 '\u2205']
REGEX_BOLD = re.compile('@+(.*?)@+')
REGEX_ITALIC = re.compile('#+(.*?)#+')
REGEX_SMALL = re.compile('\\$+(.*?)\\$+')
REGEX_SMALL_BOLD = re.compile('%+(.*?)%+')
REGEX_SUPERSCRIPT = re.compile('\\^+(.*?)\\^+')
REGEX_REMOVE_HTML_TAGS = re.compile(r'<[^>]+>')
REGEX_REPLACE_HTML_ENTITIES = re.compile(r'&[^;]+;')
REGEX_REMOVE_WHITESPACE = re.compile(r'^\s+')


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def interpunkcija(tekst, znak):
    if len(tekst) < 1:
        return tekst
    if tekst[-1] == '>' and tekst[-4] == '<' and tekst[-5] in '!"#$%&\'(*+,-./:;<=?@[\\]^_`{|}~':
        return tekst
    if tekst[-1] == '>' and tekst[-3] == '<' and tekst[-4] in '!"#$%&\'(*+,-./:;<=?@[\\]^_`{|}~':
        return tekst
    if tekst[-1] not in '!"#$%&\'(*+,-./:;<=?@[\\]^_`{|}~':  # izbaceno: >)
        return tekst + znak
    return tekst


def dvotacka(tekst):
    return interpunkcija(tekst, ':')


def tacka(tekst):
    return interpunkcija(tekst, '.')


def nbsp(tekst):
    if len(tekst) < 1:
        return tekst
    return tekst.replace(' ', '&nbsp;')


def nabrajanje(items):
    if len(items) == 0:
        return ''
    if len(items) == 1:
        return items[0]
    return ', '.join(items[:-1]) + ' и ' + items[-1]


def process_special_marks(tekst):
    for mark in SPECIAL_MARKS:
        tekst = tekst.replace(mark, f'<small>{mark}</small>')
    for znak in ['м', 'ж', 'с']:
        if tekst.startswith(f'({znak} '):
            tekst = f'(<small>{znak}</small> ' + tekst[3:]
        if tekst.startswith(f'[{znak} '):
            tekst = f'[<small>{znak}</small> ' + tekst[3:]
        if tekst.startswith(f'{znak} '):
            tekst = f'<small>{znak}</small> ' + tekst[2:]
        if tekst.endswith(f' {znak})'):
            tekst = tekst[:-3] + f' <small>{znak}</small>)'
        if tekst.endswith(f' {znak}]'):
            tekst = tekst[:-3] + f' <small>{znak}</small>]'
        if tekst.endswith(f' {znak}'):
            tekst = tekst[:-2] + f' <small>{znak}</small>'
        tekst = tekst.replace(f' {znak} ', f' <small>{znak}</small> ')
        tekst = tekst.replace(f' {znak} ', f' <small>{znak}</small> ')
        tekst = tekst.replace(f' {znak}) ', f' <small>{znak}</small>) ')
        tekst = tekst.replace(f' ({znak} ', f' (<small>{znak}</small>) ')
        tekst = tekst.replace(f' {znak}] ', f' <small>{znak}</small>] ')
        tekst = tekst.replace(f' [{znak} ', f' [<small>{znak}</small> ')
    return tekst


def process_monkey(tekst, in_italic=False):
    if in_italic:
        return REGEX_BOLD.sub('</i><b>\\1</b><i>', tekst)
    else:
        return REGEX_BOLD.sub('<b>\\1</b>', tekst)


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


def process_percent(tekst, in_italic=False):
    if in_italic:
        return REGEX_SMALL_BOLD.sub('</i><small><b>\\1</b></small><i>', tekst)
    else:
        return REGEX_SMALL_BOLD.sub('<small><b>\\1</b></small>', tekst)


def process_circumflex(tekst, in_italic=False):
    if in_italic:
        return REGEX_SUPERSCRIPT.sub('</i><sup>\\1</sup><i>', tekst)
    else:
        return REGEX_SUPERSCRIPT.sub('<sup>\\1</sup>', tekst)


def process_tags(tekst, in_italic=False):
    retval = process_monkey(
        process_dollar(
            process_hash(
                process_percent(
                    process_circumflex(tekst, in_italic), in_italic), in_italic), in_italic), in_italic)
    if retval.endswith('<i>') or retval.endswith('<b>'):
        retval = retval[:-3]
    return retval


def render_konkordanse(konkordanse):
    retval = ''
    for k in konkordanse:
        retval += f'<i>{tacka(process_tags(k.opis, True))}</i> '
        if k.publikacija:
            retval += f'{nbsp(tacka(k.publikacija.skracenica))} '
    return retval


def render_izrazi_fraze(izrazifraze):
    tekst = ''
    for izfr in izrazifraze:
        tekst += f' <b>&bull;</b> <small><b>{izfr.tekst}</b></small> '
        tekst += render_kvalifikatori(izfr.kvalifikatorfraze_set.all().order_by('redni_broj'))
        tekst += f' {tacka(process_tags(izfr.opis, False))}'
    return tekst


def render_kvalifikatori(kvalifikatori):
    tekst = ''
    for kvod in kvalifikatori:
        tekst += f' <small>{tacka(kvod.kvalifikator.skracenica)}</small> '
    return tekst


def render_kratke_kolokacije(kolokacija):
    return f'<i>{process_tags(kolokacija.tekst, True)}</i>'


def render_podznacenje(podznacenje):
    tekst = '' + render_kvalifikatori(podznacenje.kvalifikatorpodznacenja_set.all().order_by('redni_broj'))

    if podznacenje.kolokacijapodznacenja_set.count() > 0:
        tekst += f'{dvotacka(process_tags(podznacenje.tekst))} '
        tekst += ', '.join([render_kratke_kolokacije(kol) for kol in podznacenje.kolokacijapodznacenja_set.all().order_by('redni_broj')])
        tekst = tacka(tekst)
    else:
        if podznacenje.tekst:
            tekst += f'{tacka(process_tags(podznacenje.tekst))}'

    if podznacenje.konkordansa_set.count() > 0:
        tekst = tekst + ' &mdash; '
        tekst += render_konkordanse(podznacenje.konkordansa_set.all().order_by('redni_broj'))

    tekst += render_izrazi_fraze(podznacenje.izrazfraza_set.all().order_by('redni_broj'))
    return tekst


def render_znacenje(znacenje):
    tekst = '' + render_kvalifikatori(znacenje.kvalifikatorznacenja_set.all().order_by('redni_broj'))
    if znacenje.kolokacijaznacenja_set.count() > 0:
        tekst += f'{dvotacka(process_tags(znacenje.tekst))} '
        tekst += ', '.join([render_kratke_kolokacije(kol) for kol in znacenje.kolokacijaznacenja_set.all().order_by('redni_broj')])
        tekst = tacka(tekst)
    else:
        if znacenje.tekst:
            tekst += f'{tacka(process_tags(znacenje.tekst))}'

    if znacenje.konkordansa_set.count() > 0:
        tekst = tekst + ' &mdash; '
        tekst += render_konkordanse(znacenje.konkordansa_set.all().order_by('redni_broj'))
    else:
        tekst = tacka(tekst)

    tekst += render_izrazi_fraze(znacenje.izrazfraza_set.all().order_by('redni_broj'))

    if znacenje.podznacenje_set.count() > 0:
        for rbr, podznacenje in enumerate(znacenje.podznacenje_set.all().order_by('redni_broj')):
            tekst += f' <b>{AZBUKA[rbr]}.</b> ' + render_podznacenje(podznacenje)
    return tekst


def render_info(info):
    return f' {process_tags(process_special_marks(info))} '


def render_varijanta(tekst, nastavak, prezent='', opciono_se=False, rod=None):
    def zarez(text):
        return f', {text}' if text else ''

    if not tekst and not nastavak and not prezent:
        return ''
    rod_text = f' <small>{ROD[rod]}</small>' if rod else ''
    return f'<b>{tekst}{" (ce)" if opciono_se else ""}</b>' + zarez(nastavak) + rod_text + zarez(prezent)


def render_nastavci_varijante(odrednica):
    html = ''
    if odrednica.nastavak:
        html += f', {odrednica.nastavak}'
    ima_razlicit_rod = False
    if odrednica.vrsta == 0 and odrednica.rod:
        for vod in odrednica.varijantaodrednice_set.all():
            if vod.rod and vod.rod != odrednica.rod:
                ima_razlicit_rod = True
    if ima_razlicit_rod:
        html += f' <small>{ROD[odrednica.rod]}</small> '
    if odrednica.prezent:
        html += f', {odrednica.prezent}'
    if odrednica.varijantaodrednice_set.count() > 0:
        varijante = []
        for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj"):
            var = render_varijanta(vod.tekst, vod.nastavak, vod.prezent, vod.opciono_se, vod.rod)
            if var:
                varijante.append(var)
        if len(varijante) == 1:
            html += ' и ' + varijante[0]
        elif len(varijante) > 1:
            html += ', ' + nabrajanje(varijante)
    if odrednica.ijekavski or odrednica.nastavak_ij or odrednica.prezent_ij:
        html += ', <small>јек.</small> '
    if odrednica.ijekavski and odrednica.rec != odrednica.ijekavski:
        html += f'<b>{odrednica.ijekavski}</b>'
    elif odrednica.ijekavski and odrednica.rec == odrednica.ijekavski:
        html += ' и '
    if odrednica.nastavak_ij:
        html += f', {odrednica.nastavak_ij}'
    if odrednica.prezent_ij:
        html += f', {odrednica.prezent_ij}'
    if odrednica.varijantaodrednice_set.count() > 0:
        varijante = []
        for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj"):
            var = render_varijanta(vod.ijekavski, vod.nastavak_ij, vod.prezent_ij, vod.opciono_se, vod.rod)
            if var:
                varijante.append(var)
        if len(varijante) == 1:
            if odrednica.rec != odrednica.ijekavski:
                html += ' и '
            html += varijante[0]
        elif len(varijante) > 1:
            html += ', ' + nabrajanje(varijante)
    if odrednica.vrsta == 0 and not ima_razlicit_rod:
        html += f' <small>{ROD[odrednica.rod]}</small> '
    return html


def render_one(odrednica):
    if odrednica.freetext:
        return process_tags(odrednica.freetext)

    html = f'<b>{odrednica.rec}'
    if odrednica.vrsta == 1 and odrednica.opciono_se:
        html += f' (се)'
    if odrednica.rbr_homonima:
        html += f' <sup>{odrednica.rbr_homonima}</sup>'
    html += f'</b>'

    # imenica
    if odrednica.vrsta == 0:
        html += render_nastavci_varijante(odrednica)
        # html += f' <small>{ROD[odrednica.rod]}</small> '
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '

    # glagol
    if odrednica.vrsta == 1:
        html += render_nastavci_varijante(odrednica)
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        if odrednica.glagolski_vid:
            html += f' <small>{GVID[odrednica.glagolski_vid]}</small> '
        else:
            html += ' '

    # pridev
    if odrednica.vrsta == 2:
        html += render_nastavci_varijante(odrednica)
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    # prilog
    if odrednica.vrsta == 3:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>прил.</small> '
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    # predlog
    if odrednica.vrsta == 4:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>предл.</small> '
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    # zamenica
    if odrednica.vrsta == 5:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>зам.</small> '
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    # uzvik
    if odrednica.vrsta == 6:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>узв.</small> '
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    # recca
    if odrednica.vrsta == 7:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>речца</small> '
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    # veznik
    if odrednica.vrsta == 8:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>везн.</small> '
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    # broj
    if odrednica.vrsta == 9:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>број</small> '
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    # ostalo
    if odrednica.vrsta == 10:
        html += render_nastavci_varijante(odrednica)
        if odrednica.info:
            html += ' ' + render_info(odrednica.info) + ' '
        else:
            html += ' '

    html += render_kvalifikatori(odrednica.kvalifikatorodrednice_set.all().order_by('redni_broj'))
    if odrednica.znacenje_set.count() == 1:
        html += render_znacenje(odrednica.znacenje_set.first())
    else:
        for rbr, znacenje in enumerate(odrednica.znacenje_set.filter(znacenje_se=False), start=1):
            html += f' <b>{rbr}.</b> ' + render_znacenje(znacenje)
        if odrednica.znacenje_set.filter(znacenje_se=True).count() > 0:
            html += f' <b>&#9632; ~ се</b> '
            if odrednica.znacenje_set.filter(znacenje_se=True).count() == 1:
                html += render_znacenje(odrednica.znacenje_set.filter(znacenje_se=True).first())
            else:
                for rbr, znacenje in enumerate(odrednica.znacenje_set.filter(znacenje_se=True), start=1):
                    html += f' <b>{rbr}.</b> ' + render_znacenje(znacenje)
    html += render_izrazi_fraze(odrednica.izrazfraza_set.all().order_by('redni_broj'))
    return mark_safe(html)


def render_one_div(odrednica, css_class='odrednica'):
    return mark_safe(f'<div class="{css_class}" data-id="{odrednica.id}">{render_one(odrednica)}</div>')


def render_many(odrednice, css_class='odrednica'):
    return mark_safe(''.join([render_one_div(od, css_class) for od in odrednice]))


def render_to_list(odrednice, css_class='odrednica'):
    return [render_one_div(od, css_class) for od in odrednice]


def font_fetcher(url):
    if url.startswith('fonts/'):
        font_path = finders.find(url)
        font_file = open(font_path, 'r')
        return {'file_obj': font_file}
    return default_url_fetcher(url)


def render_slovo(slovo, file_format='pdf', tip_dokumenta=None):
    if not tip_dokumenta:
        tip_dokumenta = 2
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=tip_dokumenta)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal(f'Nije pronadjen tip renderovanog dokumenta: id={tip_dokumenta}')
        return
    odrednice = Odrednica.objects.filter(rec__startswith=slovo[0].lower()).filter(status_id__in=trd.statusi.values_list('id', flat=True))
    odrednice = odrednice.order_by(Collate('rec', 'utf8mb4_croatian_ci'), 'rbr_homonima')
    rendered_odrednice = [render_one(o) for o in odrednice]
    context = {'odrednice': rendered_odrednice, 'slovo': slovo.upper()}
    if file_format == 'pdf':
        return render_to_pdf(context, 'render/pdf/slovo.html', trd, opis=f'слово {slovo[0].upper()}')
    elif file_format == 'docx':
        return render_to_docx(context, 'render/docx/slovo.html', trd, opis=f'слово {slovo[0].upper()}')
    else:
        return None


def render_recnik(file_format='pdf', tip_dokumenta=None):
    if not tip_dokumenta:
        tip_dokumenta = 2
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=tip_dokumenta)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal(f'Nije pronadjen tip renderovanog dokumenta: id={tip_dokumenta}')
        return
    slova = []
    for s in AZBUKA:
        odrednice = Odrednica.objects.filter(rec__startswith=s).filter(status_id__in=trd.statusi.values_list('id', flat=True))
        odrednice = odrednice.order_by(Collate('rec', 'utf8mb4_croatian_ci'), 'rbr_homonima')
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


def count_printable_chars(odrednica):
    if not odrednica:
        return 0
    text = render_one(odrednica)
    if not text:
        return 0
    text = REGEX_REPLACE_HTML_ENTITIES.sub('.', text)
    text = REGEX_REMOVE_HTML_TAGS.sub('', text)
    text = REGEX_REMOVE_WHITESPACE.sub('', text)
    return len(text)
