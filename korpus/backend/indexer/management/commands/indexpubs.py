import logging
from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch
from publikacije.models import Publikacija, TekstPublikacije
from ...index import index_publikacija
from ...utils import init_es_connection, recreate_index, check_elasticsearch, PUB_INDEX

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Index publication(s)'

    def add_arguments(self, parser):
        parser.add_argument('--pub', type=int, nargs='?', help='Publication ID')

    def handle(self, *args, **options):
        if not check_elasticsearch():
            self.stdout.write(f'Nije dostupan Elasticsearch servis na http://{settings.ELASTICSEARCH_HOST}:9200/')
            return
        pub_id = options.get('pub')
        try:
            init_es_connection()
            if pub_id:
                publist = Publikacija.objects.filter(id=pub_id)
            else:
                publist = Publikacija.objects.all()
                recreate_index(PUB_INDEX)
            client = Elasticsearch()
            for pub in publist:
                status = index_publikacija(pub.id, client)
                if status:
                    self.stdout.write(f'Successfully indexed publication ID: {pub.id}')
                else:
                    self.stdout.write(f'Error indexing publication ID: {pub.id}')
        except Publikacija.DoesNotExist:
            raise CommandError(f'Publication with ID {pub_id} does not exist')
