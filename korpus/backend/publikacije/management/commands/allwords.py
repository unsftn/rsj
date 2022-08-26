from datetime import datetime
import json
import logging
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from publikacije.reports import all_words_from_all_pubs

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate list of all words from all publications'

    def handle(self, *args, **options):
        start_time = datetime.now()
        words = all_words_from_all_pubs()
        word = list(words.items())[0]
        print(json.dumps(words, indent=2))
        end_time = datetime.now()
        log.info(f'Generisanje trajalo ukupno {str(end_time-start_time)}')
