from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch
from reci.models import Imenica, Glagol, Pridev
from indexer.utils import init_es_connection, recreate_index, check_elasticsearch, REC_INDEX
from indexer.index import index_imenica, index_glagol, index_pridev

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Reindex database in Elasticsearch'

    def handle(self, *args, **options):
        if not check_elasticsearch():
            self.stdout.write(f'Nije dostupan Elasticsearch servis na http://{settings.ELASTICSEARCH_HOST}:9200/')
            return
        # if not init_es_connection():
        #     self.stdout.write(f'Nije inicijalizovana konekcija na Elasticsearch')
        #     return
        if not recreate_index(REC_INDEX):
            self.stdout.write(f'Nije kreiran indeks {REC_INDEX}')
            return
        start_time = datetime.now()
        client = Elasticsearch()
        self.index_rec('imenica', Imenica, index_imenica, client)
        self.index_rec('prideva', Pridev, index_pridev, client)
        self.index_rec('glagola', Glagol, index_glagol, client)
        end_time = datetime.now()
        log.info(f'Indeksiranje trajalo ukupno {str(end_time-start_time)}')

    def index_rec(self, naziv, clazz, save_func, client):
        self.stdout.write(f'Ukupno {clazz.objects.count()} {naziv} za indeksiranje.')
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
