import os
import platform
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from odrednice.models import Odrednica
from ...renderer import render_slovo


class Command(BaseCommand):
    help = 'Generate PDF for RSJ'

    def add_arguments(self, parser):
        parser.add_argument('slovo', nargs='?', type=str, default='А')
        parser.add_argument('--open', action='store_true', help='Open the file upon creation')

    def handle(self, *args, **options):
        slovo = options['slovo']
        odrednice = Odrednica.objects.filter(rec__startswith=slovo)
        file_name = render_slovo(odrednice, slovo)
        if file_name:
            pdf_file = os.path.join(settings.MEDIA_ROOT, file_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully generated PDF: {pdf_file}'))
            if options['open']:
                if platform.system() == 'Darwin':
                    subprocess.Popen(['open', pdf_file])
        else:
            self.stdout.write(self.style.ERROR('PDF file not generated'))
