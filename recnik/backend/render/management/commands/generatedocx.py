import logging
import os
import platform
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from ...renderer import render_slovo, render_recnik

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate .docx for RSJ'

    def add_arguments(self, parser):
        parser.add_argument('--letter', nargs='?', type=str)
        parser.add_argument('--type', nargs='?', type=int)
        parser.add_argument('--open', action='store_true', help='Open the file upon creation')

    def handle(self, *args, **options):
        slovo = options.get('letter')
        tip = options.get('type')
        if not tip:
            tip = 2
        if slovo:
            log.info(f'Generisanje DOCX za slovo {slovo.upper()}, tip dokumenta: {tip}')
            file_name = render_slovo(slovo, 'docx', tip)
        else:
            log.info(f'Generisanje DOCX, tip dokumenta: {tip}')
            file_name = render_recnik('docx', tip)
        if file_name:
            full_path = os.path.join(settings.MEDIA_ROOT, file_name)
            self.stdout.write(self.style.SUCCESS(f'Uspesno generisan .docx: {full_path}'))
            if options['open']:
                if platform.system() == 'Darwin':
                    subprocess.Popen(['open', full_path])
        else:
            self.stdout.write(self.style.ERROR('.docx fajl nije generisan'))
        log.info('Generisanje .docx zavrseno.')
