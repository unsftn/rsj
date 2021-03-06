from django.core.management.base import BaseCommand
from django.conf import settings
from odrednice.models import Odrednica
from publikacije.models import Publikacija
from pretraga.indexer import save_odrednica_model, save_publikacija_model, recreate_index, check_elasticsearch


class Command(BaseCommand):
    help = 'Reindex database in Elasticsearch'

    def handle(self, *args, **options):
        if not check_elasticsearch():
            self.stdout.write(f'Nije dostupan Elasticsearch servis na http://{settings.ELASTICSEARCH_HOST}:9200/')
            return
        recreate_index()
        self.stdout.write(f'Ukupno {Odrednica.objects.count()} odrednica za indeksiranje.')
        count = 0
        for odr in Odrednica.objects.all():
            if save_odrednica_model(odr):
                count += 1
            if count % 1000 == 0 and count > 0:
                self.stdout.write(f'Indeksirano {count} odrednica.')
        self.stdout.write(f'Ukupno indeksirano {count} odrednica.')
        self.stdout.write(f'Ukupno {Publikacija.objects.count()} publikacija za indeksiranje.')
        count = 0
        for pub in Publikacija.objects.all():
            if save_publikacija_model(pub):
                count += 1
            if count % 1000 == 0 and count > 0:
                self.stdout.write(f'Indeksirano {count} publikacija.')
        self.stdout.write(f'Ukupno indeksirano {count} publikacija.')

