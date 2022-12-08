from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from decider.collect import collectwords

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Collect all words from corpus for decision'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info(f'Collecting words...')
        collectwords()
        end_time = datetime.now()
        log.info(f'Time elapsed: {str(end_time-start_time)}')

