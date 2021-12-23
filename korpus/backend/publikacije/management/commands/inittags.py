import logging
from django.core.management.base import BaseCommand, CommandError
from publikacije.models import TekstPublikacije
from publikacije.processing import init_tags

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Initialize tagged texts'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Force tagging for all publications')

    def handle(self, *args, **options):
        force = options.get('force')
        count = 0
        try:
            for tp in TekstPublikacije.objects.all():
                if force or not tp.tagovan_tekst:
                    tp.tagovan_tekst = init_tags(tp.tekst)
                    tp.save()
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'Inicijalizovano {count} fragmenata.'))
        except TekstPublikacije.DoesNotExist:
            raise CommandError(f'Nema tekstova za inicijalizaciju')
