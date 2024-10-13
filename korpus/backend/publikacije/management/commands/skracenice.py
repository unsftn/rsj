from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from publikacije.fixes import fix_skracenice

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate list of all words from all publications'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info(f'Sredjivanje skracenica pokrenuto...')
        fix_skracenice()
        end_time = datetime.now()
        log.info(f'Generisanje trajalo ukupno {str(end_time-start_time)}')
