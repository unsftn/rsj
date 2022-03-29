from datetime import datetime
import logging
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from publikacije.reports import all_words_from_all_pubs_docx

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Erase texts for publication'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, nargs='?', help='Odredisni Word fajl')

    def handle(self, *args, **options):
        filename = options.get('filename') or 'report.docx'
        destdir = os.path.join(settings.MEDIA_ROOT, 'reports')
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        filepath = os.path.join(destdir, filename)
        log.info(f'Generise se izvestaj: {filepath}')
        start_time = datetime.now()
        all_words_from_all_pubs_docx(filepath)
        end_time = datetime.now()
        log.info(f'Generisanje trajalo ukupno {str(end_time-start_time)}')
