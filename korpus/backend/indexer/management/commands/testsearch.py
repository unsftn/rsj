from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from reci.models import *
from publikacije.models import *
from indexer.search import _search as search, add_latin_versions
from indexer.cyrlat import cyr_to_lat

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Testira pretragu po osnovnom obliku nasuprot pretrazi po pojedinacnim oblicima'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, help='ID reci u korpusu')
        parser.add_argument('--type', type=int, help='ID vrste reci u korpusu')

    def handle(self, *args, **options):
        word_id = options.get('id')
        word_type = options.get('type')
        try:
            if word_type == 0:
                word = Imenica.objects.get(id=word_id)
                oblici = word.oblici()
            else:
                oblici = []
            oblici = list(set(oblici))

            print(f'Oblici: {oblici}')
            print('SAMO CIRILICA')
            total = []
            for oblik in oblici:
                result = search([oblik], 150, 'word')
                total.extend(result)
                print(f'Oblik: {oblik}, pogodaka: {len(result)}')
            print(f'Ukupno pogodaka {len(total)}')

            print(f'DVA PO DVA')
            total = []
            for oblik in oblici:
                terms = [oblik, cyr_to_lat(oblik)]
                result = search(terms, 150, 'word')
                total.extend(result)
                print(f'Oblik: {terms}, pogodaka: {len(result)}')
            print(f'Ukupno pogodaka {len(total)}')

            print(f'PLUS LATINICA')
            add_latin_versions(oblici)
            total = []
            for oblik in oblici:
                result = search([oblik], 150, 'word')
                total.extend(result)
                print(f'Oblik: {oblik}, pogodaka: {len(result)}')
            print(f'Ukupno pogodaka {len(total)}')

            print(f'SVE ODJEDNOM')
            result = search(oblici, 150, 'word')
            print(f'Oblici: {oblici}, pogodaka: {len(result)}')

            counters = {o:0 for o in oblici}
            for t in TekstPublikacije.objects.all():
                for k in counters.keys():
                    counters[k] += t.tekst.lower().count(k)
            print(f'{counters}')
            print(f'Ukupno {sum([v for v in counters.values()])}')
        except Exception as ex:
            log.fatal(ex)

