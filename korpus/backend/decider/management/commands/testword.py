from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from decider.collect import *

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Collect a single word from corpus and analyze merging'

    def add_arguments(self, parser):
        parser.add_argument('--token', type=str, help='Email of user who will become owner of words with no owner')

    def handle(self, *args, **options):
        token = options.get('token')
        start_time = datetime.now()
        log.info(f'Collecting for token {token}...')
        try:
            words = collect_words()
            unify(words, token)
            for k, w in words.items():
                if k.startswith(token):
                    log.info(f'Final: {w}')
        except Exception as ex:
            log.fatal(ex)
        end_time = datetime.now()
        log.info(f'Time elapsed: {str(end_time-start_time)}')

