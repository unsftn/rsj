from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from publikacije.googlesheets import authorize, read_range

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import publication metadata from the Google sheet'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info(f'Autorizacija za Google Sheets...')
        credentials = authorize()
        log.info(f'Citanje iz Google Sheets...')
        results = read_range(credentials, settings.KORPUS_SPREADSHEET_ID, 'Korpus!A3:L5000')
        log.info('Azuriranje baze...')
        # TODO: azuriranje baze
        end_time = datetime.now()
        log.info(f'Import metapodataka trajao ukupno {str(end_time-start_time)}')
