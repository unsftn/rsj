import logging
import re
from django.core.management.base import BaseCommand, CommandError
from publikacije.models import Potkorpus, Publikacija, TekstPublikacije

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Word counts per subcorpus'

    def handle(self, *args, **options):
        for pk in Potkorpus.objects.all().union(Potkorpus.objects.none()):
            count = 0
            self.stdout.write(f'{pk.naziv}...')
            for index, tp in enumerate(TekstPublikacije.objects.filter(publikacija__potkorpus_id=pk.id)):
                count += len(re.findall(r'\w+', tp.tekst))
                if index > 0 and index % 10000 == 0:
                    self.stdout.write(f'{index}...')
            self.stdout.write(f'{pk.naziv if pk else "NEMA"}: {count}')
