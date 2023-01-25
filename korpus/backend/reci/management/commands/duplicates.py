from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from ...models import *

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Find duplicates in registered words'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info('Looking for duplicates')
        for d in find_duplicates(Imenica.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Glagol.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Pridev.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Prilog.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Predlog.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Zamenica.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Veznik.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Uzvik.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Recca.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')
        for d in find_duplicates(Broj.objects.all().order_by('id')):
            log.info(f'Duplikat: {d.osnovni_oblik()} - {d.vlasnik.puno_ime()}')

        end_time = datetime.now()
        log.info(f'Finding duplicates took {str(end_time-start_time)}')


def find_duplicates(word_list):
    seen = set()
    dupes = [x for x in word_list if x in seen or seen.add(x)]
    return dupes
