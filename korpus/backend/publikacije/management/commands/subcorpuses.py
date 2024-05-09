import logging
import re
from django.core.management.base import BaseCommand, CommandError
from publikacije.models import Potkorpus, Publikacija, TekstPublikacije

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Word counts per subcorpus'

    def handle(self, *args, **options):
        for pk in Potkorpus.objects.all().union(Potkorpus.objects.none()):
            word_count = 0
            pub_count = 0
            for tp in TekstPublikacije.objects.filter(publikacija__potkorpus_id=pk.id):
                word_count += len(re.findall(r'\w+', tp.tekst))
            pub_count = Publikacija.objects.filter(potkorpus_id=pk.id).exclude(tekstpublikacije__isnull=True).count()
            self.stdout.write(f'{pk.naziv if pk else "NEMA"}: {pub_count} {word_count}')
