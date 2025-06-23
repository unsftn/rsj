import base64
import json
import logging
import re
import tempfile
from django.conf import settings
from django.core.files import File
from django.contrib.staticfiles import finders
from django.db.models.functions import Collate
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.text.fonts import FontConfiguration
from docx import Document
from htmldocx import HtmlToDocx
from odrednice.models import *
from pretraga.rest import load_opis_from_korpus
from .models import *

log = logging.getLogger(__name__)
AZBUKA = 'абвгдђежзијклљмнњопрстћуфхцчџш'
ROD = {1: 'м', 2: 'ж', 3: 'с', 4: 'м (ж)', 5: 'ж (м)', 6: 'м (с)', 7: 'с (м)', 8: 'ж (с)', 9: 'с (ж)', 10: 'м/ж',
       11: 'м/с', 12: 'ж/с', 13: ''}
GVID = {1: 'свр.', 2: 'несвр.', 3: 'свр. и несвр.',  4: 'несвр. и свр.', 5: 'свр. (несвр)',  6: 'несвр. (свр)'}
GROD = {1: 'прел.', 2: 'непрел.', 3: 'повр.', 4: 'прел. и непрел.', 5: 'непрел. и прел.', 6: 'прел. (непрел)',
        7: 'непрел. (прел)'}
SPECIAL_MARKS = ['ак.', 'аор.', 'безл.', 'бр.', 'везн.', 'вок.', 'ген.', 'гл.им.', 'дат.', 'зам.', 'зб.', 'им.',
                 'имп.', 'импф.', 'инстр.', 'јд.', 'јек.', 'комп.', 'лок.', 'мн.', 'неодр.', 'непрел.',
                 'непром.', 'несвр.', 'ном.', 'одр.', 'оном.', 'повр.', 'пр.пр.', 'пр.сад.',
                 'предл.', 'през.', 'прел.', 'прил.', 'р.пр.', 'речца.', 'свр.', 'суп.', 'суп.мн.',
                 'трен.', 'трп.', 'трп.пр.', 'уз.повр.', 'узв.', 'уч.', 'арх.', 'гл.', 'гл.им.',
                 '\u2205']
REGEX_BOLD = re.compile('@+(.*?)@+')
REGEX_ITALIC = re.compile('#+(.*?)#+')
REGEX_SMALL = re.compile('\\$+(.*?)\\$+')
REGEX_SMALL_BOLD = re.compile('%+(.*?)%+')
REGEX_SUPERSCRIPT = re.compile('\\^+(.*?)\\^+')
REGEX_GREEN = re.compile('&+(.*?)&+')
REGEX_RED = re.compile('\\*+(.*?)\\*+')
REGEX_STRIKETHROUGH = re.compile('\\|+(.*?)\\|+')
REGEX_REMOVE_HTML_TAGS = re.compile(r'<[^>]+>')
REGEX_REPLACE_HTML_ENTITIES = re.compile(r'&[^;]+;')
REGEX_REMOVE_WHITESPACE = re.compile(r'^\s+')
AZBUKA_MAP = {letter: i for i, letter in enumerate(AZBUKA)}


def get_sort_key(item):
    text = item['skracenica'].lower()    
    # Convert each character to its position in AZBUKA or to a value
    result = []
    for char in text:
        if char in AZBUKA_MAP:
            result.append(1000 + AZBUKA_MAP[char])
        else:
            result.append(ord(char))    
    return result


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def interpunkcija(tekst, znak):
    if len(tekst) < 1:
        return tekst
    if tekst[-1] == '>' and tekst[-8] == '<' and tekst[-9] in '!"#$%&\'(*+,-./:;<=?@[\\]^_`{|}':  # izbaceno ~
        return tekst
    if tekst[-1] == '>' and tekst[-4] == '<' and tekst[-5] in '!"#$%&\'(*+,-./:;<=?@[\\]^_`{|}':  # izbaceno ~
        return tekst
    if tekst[-1] == '>' and tekst[-3] == '<' and tekst[-4] in '!"#$%&\'(*+,-./:;<=?@[\\]^_`{|}':  # izbaceno ~
        return tekst
    if tekst[-1] not in '!"#$%&\'(*+,-./:;<=?@[\\]^_`{|}':  # izbaceno: >)
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
        if tekst.startswith(f'{znak} '):
            tekst = f'<small>{znak}</small> ' + tekst[2:]
        if tekst.endswith(f' {znak}'):
            tekst = tekst[:-2] + f' <small>{znak}</small>'
        tekst = tekst.replace(f' {znak} ', f' <small>{znak}</small> ')
        tekst = tekst.replace(f' {znak} ', f' <small>{znak}</small> ')
        tekst = tekst.replace(f' {znak})', f' <small>{znak}</small>)')
        tekst = tekst.replace(f'({znak} ', f'(<small>{znak}</small> ')
        tekst = tekst.replace(f' {znak}]', f' <small>{znak}</small>]')
        tekst = tekst.replace(f'[{znak} ', f'[<small>{znak}</small> ')
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


def process_asterisk(tekst, in_italic=False):
    if in_italic:
        return REGEX_RED.sub('</i><span class="green wavy">\\1</span><i>', tekst)
    else:
        return REGEX_RED.sub('<span class="green wavy">\\1</span>', tekst)


def process_ampersand(tekst, in_italic=False):
    if in_italic:
        return REGEX_GREEN.sub('</i><span class="red wavy">\\1</span><i>', tekst)
    else:
        return REGEX_GREEN.sub('<span class="red wavy">\\1</span>', tekst)


def process_vertical_bar(tekst, in_italic=False):
    if in_italic:
        return REGEX_STRIKETHROUGH.sub('</i><span class="strike blue">\\1</span><i>', tekst)
    else:
        return REGEX_STRIKETHROUGH.sub('<span class="strike blue">\\1</span>', tekst)


def process_tags(tekst, in_italic=False):
    retval = process_vertical_bar(
        process_ampersand(
            process_asterisk(
                process_monkey(
                    process_dollar(
                        process_hash(
                            process_percent(
                                process_circumflex(tekst, in_italic), 
                                    in_italic), in_italic), in_italic), in_italic), in_italic), in_italic), in_italic)
    # if retval.endswith('<i>') or retval.endswith('<b>'):
    #     retval = retval[:-3]
    return retval


def render_konkordanse(konkordanse):
    retval = ''
    for k in konkordanse:
        retval += f'<i>{tacka(process_tags(k.opis, True))}</i> '
        if k.korpus_izvor_id:
            izvor = load_opis_from_korpus(k.korpus_izvor_id)
            if izvor:
                skracenica = izvor.get('skracenica')
                if not skracenica or skracenica == '-':
                    skracenica = f'{izvor.get("pub_id")}'
                retval += f'[{tacka(skracenica)}] '
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
        else:
            tekst = tekst.strip()

    if znacenje.konkordansa_set.count() > 0:
        tekst = tekst + ' &mdash; '
        tekst += render_konkordanse(znacenje.konkordansa_set.all().order_by('redni_broj'))
    else:
        tekst = tacka(tekst)

    tekst += render_izrazi_fraze(znacenje.izrazfraza_set.all().order_by('redni_broj'))

    if znacenje.podznacenje_set.count() > 0:
        for rbr, podznacenje in enumerate(znacenje.podznacenje_set.all().order_by('redni_broj')):
            # tekst += f' <b>{AZBUKA[rbr]}.</b> ' + render_podznacenje(podznacenje)
            tekst += f' <span class="podznacenje">{AZBUKA[rbr]}.</span> ' + render_podznacenje(podznacenje)
    return tekst


def render_info(info):
    return f' {process_tags(process_special_marks(info))} '


def render_varijanta(tekst, nastavak, prezent='', opciono_se=False, rod=None, bold=True):
    def zarez(text):
        return f', {text}' if text else ''

    def se(text, s):
        if not text:
            return text
        if text.find('(се)') != -1:
            return text
        return f'{text} (се)' if s else text

    if not tekst and not nastavak and not prezent:
        return ''
    rod_text = f' <small>{ROD[rod]}</small>' if rod else ''
    glava = f'<b>{se(tekst, opciono_se)}</b>' if bold else f'{se(tekst, opciono_se)}'
    return glava + zarez(se(nastavak, opciono_se)) + rod_text + zarez(se(prezent, opciono_se))


def render_varijante(odr, ijekavski=False):
    html = ''
    if odr.varijantaodrednice_set.count() > 0:
        if odr.ravnopravne_varijante:
            varijante = []
            for vod in odr.varijantaodrednice_set.all().order_by("redni_broj"):
                if not ijekavski:
                    var = render_varijanta(vod.tekst, vod.nastavak, vod.prezent, vod.opciono_se, vod.rod, True)
                else:
                    var = render_varijanta(vod.ijekavski, vod.nastavak_ij, vod.prezent_ij, vod.opciono_se, vod.rod, True)
                if var:
                    varijante.append(var)
            if len(varijante) == 1:
                if not ijekavski:
                    html = ' и ' + varijante[0]
                else:
                    if odr.rec != odr.ijekavski:
                        html = ' и '
                    html += varijante[0]
            elif len(varijante) > 1:
                html = ', ' + nabrajanje(varijante)
        else:
            varijante = []
            for vod in odr.varijantaodrednice_set.all().order_by("redni_broj"):
                if not ijekavski:
                    var = render_varijanta(vod.tekst, vod.nastavak, vod.prezent, vod.opciono_se, vod.rod, False)
                else:
                    var = render_varijanta(vod.ijekavski, vod.nastavak_ij, vod.prezent_ij, vod.opciono_se, vod.rod, False)
                if var:
                    varijante.append(var)
            if len(varijante) > 0:
                html = f' ({nabrajanje(varijante)})'
    return html


def render_nastavci_varijante(odrednica):
    html = ''
    if odrednica.nastavak:
        html += f', {odrednica.nastavak}'
        if odrednica.vrsta == 1 and odrednica.opciono_se:
            html += ' (се)'
    ima_razlicit_rod = False
    if odrednica.vrsta == 0 and odrednica.rod:
        for vod in odrednica.varijantaodrednice_set.all():
            if vod.rod and vod.rod != odrednica.rod:
                ima_razlicit_rod = True
    if ima_razlicit_rod:
        html += f' <small>{ROD[odrednica.rod]}</small> '
    if odrednica.prezent:
        html += f', {odrednica.prezent}'
        if odrednica.opciono_se:
            html += ' (се)'
    html += render_varijante(odrednica, False)
    # if odrednica.varijantaodrednice_set.count() > 0:
    #     varijante = []
    #     for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj"):
    #         var = render_varijanta(vod.tekst, vod.nastavak, vod.prezent, vod.opciono_se, vod.rod)
    #         if var:
    #             varijante.append(var)
    #     if len(varijante) == 1:
    #         html += ' и ' + varijante[0]
    #     elif len(varijante) > 1:
    #         html += ', ' + nabrajanje(varijante)
    if odrednica.ijekavski or odrednica.nastavak_ij or odrednica.prezent_ij:
        html += ' <small>јек.</small> '
    if odrednica.ijekavski and odrednica.rec != odrednica.ijekavski:
        html += f'<b>{odrednica.ijekavski}</b>'
        if odrednica.vrsta == 1 and odrednica.opciono_se:
            html += f' <b>(се)</b>'
    elif odrednica.ijekavski and odrednica.rec == odrednica.ijekavski:
        html += ' и '
    if odrednica.nastavak_ij:
        html += f', {odrednica.nastavak_ij}'
        if odrednica.vrsta == 1 and odrednica.opciono_se:
            html += ' (се)'
    if odrednica.prezent_ij:
        html += f', {odrednica.prezent_ij}'
        if odrednica.opciono_se:
            html += ' (се)'
    html += render_varijante(odrednica, True)
    # if odrednica.varijantaodrednice_set.count() > 0:
    #     varijante = []
    #     for vod in odrednica.varijantaodrednice_set.all().order_by("redni_broj"):
    #         var = render_varijanta(vod.ijekavski, vod.nastavak_ij, vod.prezent_ij, vod.opciono_se, vod.rod)
    #         if var:
    #             varijante.append(var)
    #     if len(varijante) == 1:
    #         if odrednica.rec != odrednica.ijekavski:
    #             html += ' и '
    #         html += varijante[0]
    #     elif len(varijante) > 1:
    #         html += ', ' + nabrajanje(varijante)
    if odrednica.vrsta == 0 and not ima_razlicit_rod and odrednica.rod:
        html += f' <small>{ROD[odrednica.rod]}</small> '
    return html


def render_one(odrednica):
    glava = f'{odrednica.rec.replace("_", " ")}'
    if odrednica.rbr_homonima:
        glava += f'<sup>{odrednica.rbr_homonima}</sup>'
    if odrednica.vrsta == 1 and odrednica.opciono_se:
        glava += f' (се)'

    if odrednica.freetext:
        return mark_safe(process_tags(odrednica.freetext)), glava

    html = f'<b>{glava}</b>'

    # imenica
    if odrednica.vrsta == 0:
        html += render_nastavci_varijante(odrednica)

    # glagol
    if odrednica.vrsta == 1:
        html += render_nastavci_varijante(odrednica)
        if odrednica.glagolski_vid:
            html += f' <small>{GVID[odrednica.glagolski_vid]}</small> '
        if odrednica.glagolski_rod and odrednica.prikazi_gl_rod:
            html += f' <small>{GROD[odrednica.glagolski_rod]}</small> '

    # pridev
    if odrednica.vrsta == 2:
        html += render_nastavci_varijante(odrednica)

    # prilog
    if odrednica.vrsta == 3:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>прил.</small> '

    # predlog
    if odrednica.vrsta == 4:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>предл.</small> '

    # zamenica
    if odrednica.vrsta == 5:
        html += render_nastavci_varijante(odrednica)
        if odrednica.podvrsta:
            html += f' <small>{odrednica.podvrsta.skracenica}</small>'
        else:
            html += f' <small>зам.</small> '

    # uzvik
    if odrednica.vrsta == 6:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>узв.</small> '

    # recca
    if odrednica.vrsta == 7:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>речца</small> '

    # veznik
    if odrednica.vrsta == 8:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>везн.</small> '

    # broj
    if odrednica.vrsta == 9:
        html += render_nastavci_varijante(odrednica)
        html += f' <small>број</small> '

    # ostalo
    if odrednica.vrsta == 10:
        html += render_nastavci_varijante(odrednica)

    html += render_kvalifikatori(odrednica.kvalifikatorodrednice_set.all().order_by('redni_broj'))
    if odrednica.info:
        html += render_info(odrednica.info)
    else:
        html += ' '

    if odrednica.znacenje_set.count() == 1:
        html += render_znacenje(odrednica.znacenje_set.first())
    else:
        if odrednica.znacenje_set.filter(znacenje_se=False).count() == 1:
            html += render_znacenje(odrednica.znacenje_set.first())
        else:
            for rbr, znacenje in enumerate(odrednica.znacenje_set.filter(znacenje_se=False), start=1):
                # html += f' <b>{rbr}.</b> ' + render_znacenje(znacenje)
                html += f' <span class="znacenje">{rbr}.</span> ' + render_znacenje(znacenje)
        if odrednica.znacenje_set.filter(znacenje_se=True).count() > 0:
            html += f' <b>&#9632; ~ се</b> '
            # html += f' <span class="znacenje">&#9632; ~ се</span> '
            if odrednica.znacenje_set.filter(znacenje_se=True).count() == 1:
                html += render_znacenje(odrednica.znacenje_set.filter(znacenje_se=True).first())
            else:
                for rbr, znacenje in enumerate(odrednica.znacenje_set.filter(znacenje_se=True), start=1):
                    # html += f' <b>{rbr}.</b> ' + render_znacenje(znacenje)
                    html += f' <span class="znacenje">{rbr}.</span> ' + render_znacenje(znacenje)
    html += render_izrazi_fraze(odrednica.izrazfraza_set.all().order_by('redni_broj'))
    glava = glava.replace('<sup>1</sup>', '¹') \
        .replace('<sup>2</sup>', '²') \
        .replace('<sup>3</sup>', '³') \
        .replace('<sup>4</sup>', '⁴') \
        .replace('<sup>5</sup>', '⁵') \
        .replace('<sup>6</sup>', '⁶') \
        .replace('<sup>7</sup>', '⁷') \
        .replace('<sup>8</sup>', '⁸') \
        .replace('<sup>9</sup>', '⁹')
    return mark_safe(html), glava


def render_one_div(odrednica, css_class='odrednica'):
    return mark_safe(f'<div class="{css_class}" data-id="{odrednica.id}">{render_one(odrednica)[0]}</div>')


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


def render_skracenice(kvalifikator):
    skracenica = f'{kvalifikator["skracenica"]}.'
    naziv = f'{kvalifikator["naziv"]}'
    return mark_safe(skracenica), mark_safe(naziv)


def render_slovo(slovo, file_format='pdf', tip_dokumenta=None, vrsta_odrednice=None):
    if not tip_dokumenta:
        tip_dokumenta = 2
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=tip_dokumenta)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal(f'Nije pronadjen tip renderovanog dokumenta: id={tip_dokumenta}')
        return
    odrednice = Odrednica.objects.filter(rec__startswith=slovo[0].lower()).filter(status_id__in=trd.statusi.values_list('id', flat=True))
    if vrsta_odrednice:
        odrednice = Odrednica.objects.filter(vrsta=vrsta_odrednice)
    odrednice = odrednice.order_by(Collate('sortable_rec', 'utf8mb4_croatian_ci'), 'rbr_homonima')
    rendered_odrednice = [render_one(o) for o in odrednice]
    context = {'odrednice': rendered_odrednice, 'slovo': slovo.upper()}
    if file_format == 'pdf':
        return render_to_pdf(context, 'render/pdf/slovo.html', trd, opis=f'слово {slovo[0].upper()}')
    elif file_format == 'docx':
        return render_to_docx(context, 'render/docx/slovo.html', trd, opis=f'слово {slovo[0].upper()}')
    else:
        return None


def get_json_data(filename):
    name = f'render/templates/render/pdf/{filename}.json'
    file_path = os.path.join(settings.BASE_DIR, name)
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file) 
    return data


def render_predgovor():
    name = 'render/templates/render/pdf/predgovor.txt'
    file_path = os.path.join(settings.BASE_DIR, name)
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()
    return process_tags(data)


def load_image_as_base64(filename):
    try:
        file_path = os.path.join(settings.BASE_DIR, filename)
        with open(file_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        log.error(f'Image file not found: {filename}')
        return ''


def render_recnik(file_format='pdf', tip_dokumenta=None, vrsta_odrednice=None):
    if not tip_dokumenta:
        tip_dokumenta = 2
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=tip_dokumenta)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal(f'Nije pronadjen tip renderovanog dokumenta: id={tip_dokumenta}')
        return
    
    impresum = []
    impresum_context = []
    impresum = get_json_data("impresum")
    
    def get_full_name(ime):
        full_name = ime["ime"] + " " + ime["prezime"].upper()
        return mark_safe(f'{full_name}')
    
    impresum_context.append({
        "izradili": [get_full_name(i) for i in impresum["izradili"]],
        "uredili": [get_full_name(i) for i in impresum["uredili"]],
        "recezenti": [get_full_name(i) for i in impresum["recezenti"]],
        "copyright": mark_safe(f'{impresum["copyright"]}'),
        "napomena": mark_safe(f'{impresum["napomena"]}')
    })
    
    predgovor = render_predgovor()
    
    slova = []
    log.info('Generisanje odrednica...')
    sve_odrednice = Odrednica.objects.filter(status_id__in=trd.statusi.values_list('id', flat=True))
    for s in AZBUKA:
        odrednice = Odrednica.objects.filter(rec__startswith=s).filter(status_id__in=trd.statusi.values_list('id', flat=True))
        if vrsta_odrednice:
            odrednice = odrednice.filter(vrsta=vrsta_odrednice)
        odrednice = odrednice.order_by(Collate('sortable_rec', 'utf8mb4_croatian_ci'), 'rbr_homonima')
        slova.append({
            'slovo': s.upper(),
            'odrednice': [render_one(o) for o in odrednice]
        }) 
    slova = [s for s in slova if len(s['odrednice']) > 0]

    # filtriranje koriscenih kvalifikatora
    kvalifikatori = []
    kvalifikatori_odrednice = Kvalifikator.objects.filter(kvalifikatorodrednice__odrednica__in=sve_odrednice).values('skracenica', 'naziv', 'id').distinct()
    kvalifikatori_fraze = Kvalifikator.objects.filter(kvalifikatorfraze__izrazfraza__odrednica__in=sve_odrednice).values('skracenica', 'naziv', 'id').distinct()
    kvalifikatori_podznacenja = Kvalifikator.objects.filter(kvalifikatorpodznacenja__podznacenje__znacenje__odrednica__in=sve_odrednice).values('skracenica', 'naziv', 'id').distinct()
    kvalifikatori_znacenja = Kvalifikator.objects.filter(kvalifikatorznacenja__znacenje__odrednica__in=sve_odrednice).values('skracenica', 'naziv', 'id').distinct()
    skracenice = kvalifikatori_odrednice | kvalifikatori_fraze | kvalifikatori_podznacenja | kvalifikatori_znacenja
    for s in skracenice:
        kvalifikatori.append({
            'skracenica': mark_safe(f'{s["skracenica"]}.'),
            'naziv': mark_safe(f'{s["naziv"]}')
        })
            
    # znakovi interpunkcije
    interpunkcija = []
    interpunkcija = get_json_data("interpunkcija")
    for i in interpunkcija["interpunkcija"]:
         kvalifikatori.append({
            'skracenica': mark_safe(f'{i["znak"]}'),
            'naziv': mark_safe(f'{i["objasnjenje"]}')
        })

    konkordance_znacenja = Konkordansa.objects.filter(znacenje__odrednica__in=sve_odrednice).values('korpus_izvor_id').distinct()
    konkordance_podznacenja = Konkordansa.objects.filter(podznacenje__znacenje__odrednica__in=sve_odrednice).values('korpus_izvor_id').distinct()
    konkordance = (konkordance_znacenja | konkordance_podznacenja).distinct()
    izvori = []
    for k in konkordance:
        izvor = load_opis_from_korpus(k['korpus_izvor_id'])
        if izvor:
            skracenica = izvor.get('skracenica')
            if not skracenica or skracenica == '-' or skracenica == '.':
                skracenica = f'[{izvor.get("pub_id")}]'
            izvori.append({
                'skracenica': mark_safe(f'{skracenica}'),
                'opis': mark_safe(f'{izvor.get("opis")}')
            })
    izvori = [dict(t) for t in {tuple(d.items()) for d in izvori}]
    izvori = sorted(izvori, key=get_sort_key)

    matica_logo = load_image_as_base64('static/MS.jpg')

    context = {
        'slova': slova, 
        'kvalifikatori': kvalifikatori, 
        'impresum': impresum_context[0], 
        'predgovor': predgovor,
        'izvori': izvori,
        'matica_logo': matica_logo,
    }
    
    log.info(f'Generisanje fajla, tip: {file_format}...')
    if file_format == 'pdf':
        return render_to_pdf(context, 'render/pdf/recnik2.html', trd)
    elif file_format == 'docx':
        return render_to_docx(context, 'render/docx/recnik.html', trd)
    else:
        return None


def render_to_pdf(context, template, doc_type, opis=''):
    tpl = get_template(template)
    html_text = tpl.render(context)
    with open(os.path.join(settings.MEDIA_ROOT, 'output.html'), 'w', encoding='utf-8') as f:
        f.write(html_text)
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
    # return ''


def render_for_accents(tip_dokumenta, output_file):
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=tip_dokumenta)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal(f'Nije pronadjen tip renderovanog dokumenta: id={tip_dokumenta}')
        return
    sve_odrednice = Odrednica.objects.filter(
        status_id__in=trd.statusi.values_list('id', flat=True)) \
            .order_by(Collate('sortable_rec', 'utf8mb4_croatian_ci'), 'rbr_homonima')
    glave = []
    for odrednica in sve_odrednice:
        glava = f'{odrednica.rec.replace("_", " ")}'
        if odrednica.rbr_homonima:
            glava += f'<sup>{odrednica.rbr_homonima}</sup>'
        if odrednica.vrsta == 1 and odrednica.opciono_se:
            glava += f' (се)'
        html = f'<b>{glava}</b>'
        html += render_nastavci_varijante(odrednica)
        glave.append(mark_safe(html))
    
    tpl = get_template('render/pdf/akcent.html')
    html_text = tpl.render({'glave': glave})
    html = HTML(string=html_text, url_fetcher=font_fetcher)
    css_file_name = finders.find('print-styles/slovo.css')
    with open(css_file_name, 'r') as css_file:
        css_text = css_file.read()
    font_config = FontConfiguration()
    css = CSS(string=css_text, font_config=font_config, url_fetcher=font_fetcher)
    with open(output_file, 'wb') as output_pdf:
        html.write_pdf(output_pdf, stylesheets=[css], font_config=font_config)


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
