from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from publikacije.fixes import fix_skracenice_235

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Popravljanje skracenica v2 za novinski, razgovorni i administrativni potkorpus'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info(f'Sredjivanje skracenica pokrenuto...')
        fix_skracenice_235()
        end_time = datetime.now()
        log.info(f'Sredjivanje trajalo ukupno {str(end_time-start_time)}')
