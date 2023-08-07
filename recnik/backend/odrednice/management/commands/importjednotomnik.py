import logging
import os
from django.core.management.base import BaseCommand, CommandError
import docx
from odrednice.models import Odrednica, Znacenje, Podznacenje
from odrednice.imports.jednotomnik import process_file, import_entries

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import znacenja iz teksta jednotomnika'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Tekstualni fajl jednotomnika')

    def handle(self, *args, **options):
        file = options.get('file')
        if not os.path.exists(file):
            raise CommandError(f'Fajl {file} ne postoji.')
        entries = process_file(file)
        log.info(f'Procitano {len(entries)} odrednica.')
        odrednica, znacenja, podznacenja = import_entries(entries)
        log.info(f'Izmenjeno {odrednica} odrednica, dodato {znacenja} znacenja i {podznacenja} podznacenja.')
