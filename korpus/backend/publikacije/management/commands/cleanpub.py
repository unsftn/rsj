import logging
from django.core.management.base import BaseCommand, CommandError
from publikacije.models import Publikacija, TekstPublikacije

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Erase texts for publication'

    def add_arguments(self, parser):
        parser.add_argument('pub_id', type=int, help='Publication ID')

    def handle(self, *args, **options):
        pub_id = options.get('pub_id')
        try:
            publikacija = Publikacija.objects.get(id=pub_id)
            TekstPublikacije.objects.filter(publikacija=publikacija).delete()
            self.stdout.write(f'Successfully deleted texts for publication ID: {pub_id}')
        except Publikacija.DoesNotExist:
            raise CommandError(f'Publication with ID {pub_id} does not exist')
