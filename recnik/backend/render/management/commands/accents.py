from datetime import datetime, timedelta
import logging
import os
import platform
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from ...models import RenderovaniDokument
from ...renderer import render_for_accents

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate PDF for accentuation'

    def add_arguments(self, parser):
        parser.add_argument('--type', nargs='?', type=int, help='Dictionary type (see tipovi renderovanog dokumenta)')
        parser.add_argument('--open', action='store_true', help='Open the file upon creation')

    def handle(self, *args, **options):
        tip = options.get('type') or 2
        pdf_file = os.path.join(settings.MEDIA_ROOT, f'accents_{tip}.pdf')
        log.info(f'Tip generisanja: {tip}')
        log.info(f'PDF fajl: {pdf_file}')
        start_time = datetime.now()
        render_for_accents(tip, pdf_file)
        end_time = datetime.now()
        self.stdout.write(self.style.SUCCESS(f'Generisanje trajalo ukupno {str(end_time-start_time)}'))
        if options['open']:
            if platform.system() == 'Darwin':
                subprocess.Popen(['open', pdf_file])
