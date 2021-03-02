from django.core.management.base import BaseCommand, CommandError
from elasticsearch_dsl import Search, analyzer, Index
from odrednice.models import Odrednica
from pretraga.models import OdrednicaDocument, KorpusDocument
from pretraga.indexer import save_odrednica_model, recreate_index

class Command(BaseCommand):
    help = 'Reindex database in Elasticsearch'

    def handle(self, *args, **options):
        recreate_index()
        self.stdout.write(f'Ukupno {Odrednica.objects.count()} odrednica za indeksiranje.')
        count = 0
        for odr in Odrednica.objects.all():
            save_odrednica_model(odr)
            count += 1
            if count % 1000 == 0:
                self.stdout.write(f'Indeksirano {count} odrednica.')
        self.stdout.write(f'Ukupno indeksirano {count} odrednica.')
