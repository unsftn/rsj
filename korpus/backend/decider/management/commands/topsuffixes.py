from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from weasyprint import HTML, CSS, default_url_fetcher
from weasyprint.text.fonts import FontConfiguration
from decider.collect import *

log = logging.getLogger(__name__)


def font_fetcher(url):
    if url.startswith('fonts/'):
        font_path = finders.find(url)
        font_file = open(font_path, 'r')
        return {'file_obj': font_file}
    return default_url_fetcher(url)


class Command(BaseCommand):
    help = 'Collect top n words by frequency with the given suffix'

    def add_arguments(self, parser):
        parser.add_argument('--suffix', type=str, help='Word suffix to search for')
        parser.add_argument('--limit', type=int, help='Number of top words by frequency to collect')
        parser.add_argument('--output', type=str, help='Output file path')

    def handle(self, *args, **options):
        suffix = options.get('suffix')
        limit = options.get('limit')
        output_file = options.get('output')
        start_time = datetime.now()
        log.info(f'Collecting top {limit} words by frequency for suffix -{suffix}...')
        words = []
        try:
            for rzo in RecZaOdluku.objects.all():
                if rzo.tekst.endswith(suffix):
                    rzo.u_rsj = "да" if rzo.recnik_id else "не"
                    words.append(rzo)
            log.info(f'Found {len(words)} words with suffix -{suffix}')
            words.sort(key=lambda x: x.broj_pojavljivanja, reverse=True)
            log.info(f'Sorted words by frequency')
            # with open(output_file, 'w') as f:
            #     for i in range(limit):
            #         f.write(f'{words[i].tekst} {words[i].broj_pojavljivanja} {"да" if words[i].recnik_id else "не"}\n')

            context = {
                'words': words[:limit],
                'suffix': suffix,
                'limit': limit,
                'datum': datetime.now().strftime('%d.%m.%Y.'),
            }
            tpl = get_template('decider/topsuffix.html')
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
            filename = os.path.join(dir, output_file)
            html.write_pdf(filename, stylesheets=[css], font_config=font_config)
        except Exception as ex:
            log.fatal(ex)
        end_time = datetime.now()
        log.info(f'Time elapsed: {str(end_time-start_time)}')

