from datetime import datetime, timedelta
import logging
import os
import platform
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from ...models import RenderovaniDokument
from ...renderer import render_slovo, render_recnik

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate PDF for RSJ'

    def add_arguments(self, parser):
        parser.add_argument('--letter', nargs='?', type=str, help='Dictionary letter to generate')
        parser.add_argument('--type', nargs='?', type=int, help='Dictionary type (see tipovi renderovanog dokumenta)')
        parser.add_argument('--format', nargs='?', type=str, help='File format: pdf or docx')
        parser.add_argument('--expired', nargs='?', type=int, help='Remove generated files older than the given number of days')
        parser.add_argument('--open', action='store_true', help='Open the file upon creation')

    def handle(self, *args, **options):
        slovo = options.get('letter')
        tip = options.get('type') or 2
        stari = options.get('expired') or 60
        format = options.get('format') or 'pdf'
        log.info(f'Fromat fajla: {format}')
        log.info(f'Brisanje fajlova starijih od (dana): {stari}')
        log.info(f'Tip generisanja: {tip}')
        log.info(f'Sadrzaj generisanja: {("slovo "+slovo) if slovo else "sva slova"}')
        start_time = datetime.now()
        if slovo:
            file_name = render_slovo(slovo, format, tip)
        else:
            file_name = render_recnik(format, tip)
        if file_name:
            pdf_file = os.path.join(settings.MEDIA_ROOT, file_name)
            self.stdout.write(self.style.SUCCESS(f'Uspesno generisan fajl: {pdf_file}'))
            cutoff_date = timezone.now() - timedelta(days=stari)
            log.info(f'Brisanje generisanih fajlova starijih od {cutoff_date}')
            RenderovaniDokument.objects.filter(vreme_rendera__lt=cutoff_date).delete()
            if options['open']:
                if platform.system() == 'Darwin':
                    subprocess.Popen(['open', pdf_file])
        else:
            self.stdout.write(self.style.ERROR('Fajl nije generisan.'))
        end_time = datetime.now()
        log.info(f'Generisanje trajalo ukupno {str(end_time-start_time)}')
