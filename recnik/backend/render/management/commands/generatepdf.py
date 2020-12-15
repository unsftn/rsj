from django.core.management.base import BaseCommand, CommandError

from ...views import FAKE_ODREDNICE
from ...renderer import render_slovo


class Command(BaseCommand):
    help = 'Generate PDF for RSJ'

    def add_arguments(self, parser):
        parser.add_argument('slovo', nargs='?', type=str, default='A')

    def handle(self, *args, **options):
        slovo = options['slovo']
        odrednice = [FAKE_ODREDNICE[key] for key in sorted(FAKE_ODREDNICE.keys())]
        file_name = render_slovo(odrednice, slovo)
        if file_name:
            self.stdout.write(self.style.SUCCESS('Successfully generated PDF'))
        else:
            self.stdout.write(self.style.ERROR('PDF file not generated'))
