import logging
import os
import platform
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from odrednice.models import Odrednica
from ...renderer import render_slovo, render_recnik

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate PDF for RSJ'

    def add_arguments(self, parser):
        parser.add_argument('slovo', nargs='?', type=str)
        parser.add_argument('--open', action='store_true', help='Open the file upon creation')

    def handle(self, *args, **options):
        slovo = options.get('slovo')
        if slovo:
            log.info(f'Generisanje PDFa za slovo {slovo.upper()}')
            file_name = render_slovo(slovo)
        else:
            log.info(f'Generisanje PDFa za ceo recnik')
            file_name = render_recnik()
        if file_name:
            pdf_file = os.path.join(settings.MEDIA_ROOT, file_name)
            self.stdout.write(self.style.SUCCESS(f'Uspesno generisan PDF: {pdf_file}'))
            if options['open']:
                if platform.system() == 'Darwin':
                    subprocess.Popen(['open', pdf_file])
        else:
            self.stdout.write(self.style.ERROR('PDF fajl nije generisan'))
        log.info('Generisanje PDFa zavrseno.')
