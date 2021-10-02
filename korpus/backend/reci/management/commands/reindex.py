from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import Imenica, Glagol, Pridev
from ...indexer import index_imenica, index_glagol, index_pridev, recreate_index, check_elasticsearch

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Reindex database in Elasticsearch'

    def handle(self, *args, **options):
        if not check_elasticsearch():
            self.stdout.write(f'Nije dostupan Elasticsearch servis na http://{settings.ELASTICSEARCH_HOST}:9200/')
            return
        recreate_index()
        start_time = datetime.now()
        self.index_rec('imenica', Imenica, index_imenica)
        self.index_rec('glagola', Glagol, index_glagol)
        self.index_rec('prideva', Pridev, index_pridev)
        end_time = datetime.now()
        log.info(f'Indeksiranje trajalo ukupno {str(end_time-start_time)}')

    def index_rec(self, naziv, clazz, save_func):
        self.stdout.write(f'Ukupno {Imenica.objects.count()} {naziv} za indeksiranje.')
        count = 0
        for rec in clazz.objects.all():
            if save_func(rec):
                count += 1
            if count % 1000 == 0 and count > 0:
                self.stdout.write('.', ending='')
            if count % 10000 == 0 and count > 0:
                self.stdout.write(f'{count}')
        self.stdout.write(self.style.SUCCESS(f'\nUkupno indeksirano {count} {naziv}.'))
