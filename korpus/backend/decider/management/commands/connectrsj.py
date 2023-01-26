from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from decider.collect import connect_to_rsj

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Connect words from corpus to RSJ'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info(f'Connecting words to RSJ...')
        connect_to_rsj()
        end_time = datetime.now()
        log.info(f'Time elapsed: {str(end_time-start_time)}')

