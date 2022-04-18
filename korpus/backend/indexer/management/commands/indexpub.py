import logging
from django.core.management.base import BaseCommand, CommandError
from publikacije.models import Publikacija, TekstPublikacije
from ...index import index_publikacija

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Index publication(s)'

    def add_arguments(self, parser):
        parser.add_argument('pub_id', type=int, help='Publication ID')

    def handle(self, *args, **options):
        pub_id = options.get('pub_id')
        try:
            Publikacija.objects.get(id=pub_id)
            status = index_publikacija(pub_id)
            if status:
                self.stdout.write(f'Successfully indexed publication ID: {pub_id}')
            else:
                self.stdout.write(f'Error indexing publication ID: {pub_id}')
        except Publikacija.DoesNotExist:
            raise CommandError(f'Publication with ID {pub_id} does not exist')
