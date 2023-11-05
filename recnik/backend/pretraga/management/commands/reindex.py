from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from odrednice.models import Odrednica
from pretraga.indexer import save_odrednica, recreate_index, check_elasticsearch
from pretraga.config import get_es_client

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Reindex database in Elasticsearch'

    def handle(self, *args, **options):
        if not check_elasticsearch():
            self.stdout.write(f'Nije dostupan Elasticsearch servis na {settings.ELASTICSEARCH_HOST}')
            return
        recreate_index()
        self.stdout.write(f'Ukupno {Odrednica.objects.count()} odrednica za indeksiranje.')
        start_time = datetime.now()
        client = get_es_client()
        count = 0
        for odr in Odrednica.objects.all():
            if save_odrednica(odr, client):
                count += 1
            if count % 1000 == 0 and count > 0:
                self.stdout.write('.', ending='')
                self.stdout.flush()
            if count % 10000 == 0 and count > 0:
                self.stdout.write(f'{count}')
                self.stdout.flush()
        self.stdout.write(self.style.SUCCESS(f'\nUkupno indeksirano {count} odrednica.'))
        end_time = datetime.now()
        log.info(f'Indeksiranje trajalo ukupno {str(end_time-start_time)}')
