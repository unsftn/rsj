from datetime import datetime
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from publikacije.models import Publikacija
from ...index import index_naslov
from ...utils import get_es_client, recreate_index, check_elasticsearch, NASLOV_INDEX, push_highlighting_limit

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Index publication titles'

    def handle(self, *args, **options):
        if not check_elasticsearch():
            log.fatal(f'Nije dostupan Elasticsearch servis na {settings.ELASTICSEARCH_HOST}')
            return
        try:
            if not recreate_index(NASLOV_INDEX):
                log.fatal(f'Nije kreiran indeks {NASLOV_INDEX}')
                return
            start_time = datetime.now()
            client = get_es_client()
            count = 0
            for pub in Publikacija.objects.all():
                status = index_naslov(pub.id, client)
                if not status:
                    log.info(f'Greska prilikom indeksiranja naslova ID: {pub.id}')
                count += 1
                if count % 1000 == 0 and count > 0:
                    self.stdout.write('.', ending='')
                    self.stdout.flush()
                if count % 10000 == 0 and count > 0:
                    self.stdout.write(f'{count}')
                    self.stdout.flush()
            if count % 10000 != 0 and count > 1000:
                self.stdout.write('')
            log.info(f'Indeksirano {count} naslova.')                
            push_highlighting_limit()
            end_time = datetime.now()
            log.info(f'Indeksiranje trajalo ukupno {str(end_time-start_time)}')
        except Exception as ex:
            print(ex)
            raise CommandError(ex)
