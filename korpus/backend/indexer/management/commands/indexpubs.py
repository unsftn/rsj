import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from elasticsearch import Elasticsearch
from publikacije.models import Publikacija, TekstPublikacije
from ...index import index_publikacija
from ...utils import get_es_client, recreate_index, check_elasticsearch, PUB_INDEX

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Index publication(s)'

    def add_arguments(self, parser):
        parser.add_argument('--pub', type=int, nargs='?', help='Publication ID')

    def handle(self, *args, **options):
        if not check_elasticsearch():
            self.stdout.write(f'Nije dostupan Elasticsearch servis na {settings.ELASTICSEARCH_HOST}')
            return
        pub_id = options.get('pub')
        try:
            if pub_id:
                publist = Publikacija.objects.filter(id=pub_id)
            else:
                publist = Publikacija.objects.all()
            if not recreate_index(PUB_INDEX):
                self.stdout.write(f'Nije kreiran indeks {PUB_INDEX}')
                return
            client = get_es_client()
            for pub in publist:
                status = index_publikacija(pub.id, client)
                if status:
                    self.stdout.write(f'Uspesno indeksirana publikacija ID: {pub.id}')
                else:
                    self.stdout.write(f'Greska prilikom indeksiranja publikacije ID: {pub.id}')
        except Publikacija.DoesNotExist:
            raise CommandError(f'Publikacija sa ID {pub_id} ne postoji')
        except Exception as ex:
            print(ex)
            raise CommandError(ex)
