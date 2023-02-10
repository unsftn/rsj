import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from publikacije.models import Publikacija
from ...index import index_naslov
from ...utils import get_es_client, recreate_index, check_elasticsearch, NASLOV_INDEX

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
            client = get_es_client()
            count = 0
            for pub in Publikacija.objects.all():
                status = index_naslov(pub.id, client)
                if not status:
                    log.info(f'Greska prilikom indeksiranja naslova ID: {pub.id}')
                count += 1
            log.info(f'Indeksirano {count} naslova.')                
        except Exception as ex:
            print(ex)
            raise CommandError(ex)
