import logging
from django.core.management.base import BaseCommand, CommandError
from publikacije.models import Publikacija, TekstPublikacije
from ...index import index_publikacija
from ...utils import recreate_index, PUB_INDEX

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Index publication(s)'

    def add_arguments(self, parser):
        parser.add_argument('--pub', type=int, nargs='?', help='Publication ID')

    def handle(self, *args, **options):
        pub_id = options.get('pub')
        try:
            if pub_id:
                publist = Publikacija.objects.filter(id=pub_id)
            else:
                publist = Publikacija.objects.all()
                recreate_index(PUB_INDEX)
            for pub in publist:
                status = index_publikacija(pub.id)
                if status:
                    self.stdout.write(f'Successfully indexed publication ID: {pub.id}')
                else:
                    self.stdout.write(f'Error indexing publication ID: {pub.id}')
        except Publikacija.DoesNotExist:
            raise CommandError(f'Publication with ID {pub_id} does not exist')
