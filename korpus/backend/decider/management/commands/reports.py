from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from decider.reports import generisi_predefinisane

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate all predefined reports'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info(f'Generating reports...')
        generisi_predefinisane()
        end_time = datetime.now()
        log.info(f'Time elapsed: {str(end_time-start_time)}')

