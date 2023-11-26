from datetime import datetime
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from elasticsearch import Elasticsearch
from publikacije.models import Publikacija, TekstPublikacije
from ...index import index_publikacija
from ...utils import get_es_client, recreate_index, check_elasticsearch, PUB_INDEX, REVERSE_INDEX, push_highlighting_limit

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Index publication(s)'

    def add_arguments(self, parser):
        parser.add_argument('--pub', type=int, nargs='?', help='Publication ID')

    def handle(self, *args, **options):
        if not check_elasticsearch():
            log.fatal(f'Nije dostupan Elasticsearch servis na {settings.ELASTICSEARCH_HOST}')
            return
        pub_id = options.get('pub')
        try:
            if pub_id:
                publist = Publikacija.objects.filter(id=pub_id)
            else:
                publist = Publikacija.objects.all()
            if not recreate_index(PUB_INDEX):
                log.fatal(f'Nije kreiran indeks {PUB_INDEX}')
                return
            if not recreate_index(REVERSE_INDEX):
                log.fatal(f'Nije kreiran indeks {REVERSE_INDEX}')
                return
            start_time = datetime.now()
            client = get_es_client()
            count = 0
            for pub in publist:
                status = index_publikacija(pub.id, client)
                if not status:
                    log.info(f'Greska prilikom indeksiranja publikacije ID: {pub.id}')
                count += 1
                if count % 1000 == 0 and count > 0:
                    self.stdout.write('.', ending='')
                    self.stdout.flush()
                if count % 10000 == 0 and count > 0:
                    self.stdout.write(f'{count}')
                    self.stdout.flush()
            if count % 10000 != 0 and count > 1000:
                self.stdout.write('')
            log.info(f'Indeksirano {count} publikacija.')
            end_time = datetime.now()
            log.info(f'Indeksiranje trajalo ukupno {str(end_time-start_time)}')
            push_highlighting_limit()
        except Publikacija.DoesNotExist:
            raise CommandError(f'Publikacija sa ID {pub_id} ne postoji')
        except Exception as ex:
            log.fatal(ex)
            raise CommandError(ex)
