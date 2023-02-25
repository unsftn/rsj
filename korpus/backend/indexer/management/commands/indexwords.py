from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from reci.models import *
from indexer.index import *
from indexer.utils import get_es_client, recreate_index, check_elasticsearch, REC_INDEX, push_highlighting_limit

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Reindex database in Elasticsearch'

    def handle(self, *args, **options):
        log.info('Indeksiranje reci...')
        if not check_elasticsearch():
            self.stdout.write(f'Nije dostupan Elasticsearch servis na {settings.ELASTICSEARCH_HOST}')
            return
        if not recreate_index(REC_INDEX):
            self.stdout.write(f'Nije kreiran indeks {REC_INDEX}')
            return
        start_time = datetime.now()
        client = get_es_client()
        self.index_rec('imenica', Imenica, index_imenica, client)
        self.index_rec('prideva', Pridev, index_pridev, client)
        self.index_rec('glagola', Glagol, index_glagol, client)
        self.index_rec('zamenica', Zamenica, index_zamenica, client)
        self.index_rec('priloga', Prilog, index_prilog, client)
        self.index_rec('predloga', Predlog, index_predlog, client)
        self.index_rec('veznika', Veznik, index_veznik, client)
        self.index_rec('brojeva', Broj, index_broj, client)
        self.index_rec('recci', Recca, index_recca, client)
        self.index_rec('uzvika', Uzvik, index_uzvik, client)
        push_highlighting_limit()
        end_time = datetime.now()
        log.info(f'Indeksiranje trajalo ukupno {str(end_time-start_time)}')

    def index_rec(self, naziv, clazz, save_func, client):
        self.stdout.write(f'Ukupno {clazz.objects.count()} {naziv} za indeksiranje.')
        log.info(f'Ukupno {clazz.objects.count()} {naziv} za indeksiranje.')
        count = 0
        for rec in clazz.objects.all():
            if save_func(rec, client):
                count += 1
            if count % 1000 == 0 and count > 0:
                self.stdout.write('.', ending='')
                self.stdout.flush()
            if count % 10000 == 0 and count > 0:
                self.stdout.write(f'{count}')
                self.stdout.flush()
        if count % 10000 != 0 and count > 1000:
            self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Ukupno indeksirano {count} {naziv}.'))
        log.info(f'Ukupno indeksirano {count} {naziv}.')
