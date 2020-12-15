import logging
import os
import tempfile
from django.core.files import File
from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.fonts import FontConfiguration
from .models import *

log = logging.getLogger(__name__)


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def font_fetcher(url):
    print(url)
    if url.startswith('fonts/'):
        font_path = finders.find(url)
        print(f'loading font: {font_path}')
        font_file = open(font_path, 'r')
        return {'file_obj': font_file}
    return default_url_fetcher(url)


def render_one(odrednica):
    return mark_safe(odrednica)


def render_many(odrednice, css_class='odrednica'):
    return mark_safe(''.join([f'<div class="{css_class}"{od}></div>' for od in odrednice]))


def render_slovo(odrednice, slovo):
    try:
        trd = TipRenderovanogDokumenta.objects.get(id=1)
    except TipRenderovanogDokumenta.DoesNotExist:
        log.fatal('Nije pronadjen tip renderovanog dokumenta: id=1')
        return None
    template = get_template('render/odrednice.html')
    context = {'odrednice': odrednice, 'slovo': slovo}
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
