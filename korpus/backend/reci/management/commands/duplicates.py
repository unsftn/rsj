from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from ...models import *

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Pronalazi duplikate u obradjenim recima'

    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true')

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info('Pronalazenje duplikata...')
        imenice = find_duplicates(Imenica.objects.all().order_by('id'))
        glagoli = find_duplicates(Glagol.objects.all().order_by('id'))
        pridevi = find_duplicates(Pridev.objects.all().order_by('id'))
        prilozi = find_duplicates(Prilog.objects.all().order_by('id'))
        predlozi = find_duplicates(Predlog.objects.all().order_by('id'))
        zamenice = find_duplicates(Zamenica.objects.all().order_by('id'))
        veznici = find_duplicates(Veznik.objects.all().order_by('id'))
        uzvici = find_duplicates(Uzvik.objects.all().order_by('id'))
        recce = find_duplicates(Recca.objects.all().order_by('id'))
        brojevi = find_duplicates(Broj.objects.all().order_by('id'))
        
        log.info('Lista duplikata po vrsti reci:')
        print_duplicates(imenice)
        print_duplicates(glagoli)
        print_duplicates(pridevi)
        print_duplicates(prilozi)
        print_duplicates(predlozi)
        print_duplicates(zamenice)
        print_duplicates(veznici)
        print_duplicates(uzvici)
        print_duplicates(recce)
        print_duplicates(brojevi)

        log.info('Lista duplikata po vlasniku:')
        all_dupes = []
        all_dupes.extend(imenice)
        all_dupes.extend(glagoli)
        all_dupes.extend(pridevi)
        all_dupes.extend(prilozi)
        all_dupes.extend(predlozi)
        all_dupes.extend(zamenice)
        all_dupes.extend(veznici)
        all_dupes.extend(uzvici)
        all_dupes.extend(recce)
        all_dupes.extend(brojevi)
        all_dupes = sorted(all_dupes, key=lambda x: x.vlasnik.puno_ime())
        print_duplicates(all_dupes)

        end_time = datetime.now()
        log.info(f'Pronalazenje duplikata trajalo {str(end_time-start_time)}')

        if options.get('delete'):
            log.info(f'Zapoceto uklanjanje duplikata...')
            start_time = datetime.now()
            for dup in all_dupes:
                dup.delete()
            end_time = datetime.now()
            log.info(f'Uklanjanje duplikata trajalo {str(end_time-start_time)}')


def find_duplicates(word_list):
    seen = set()
    dupes = [x for x in word_list if x in seen or seen.add(x)]
    return dupes


def print_duplicates(word_list):
    for w in word_list:
        log.info(f'{word_type(w)}:{w.id}:{w.osnovni_oblik()}:{w.vlasnik.email}:{w.vlasnik.puno_ime()}')


def word_type(word):
    return word.__class__.__name__.lower()
