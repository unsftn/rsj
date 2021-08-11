import logging
from django.core.management.base import BaseCommand
from odrednice.models import Odrednica
from odrednice.text import remove_punctuation

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate sortable words'

    def handle(self, *args, **options):
        log.info('Generisanje reči za sortiranje')

        odrednice = Odrednica.objects.all()

        for odr in odrednice:
            odr.sortable_rec = remove_punctuation(odr.rec)
            odr.save()

        self.style.SUCCESS(f'Zavrseno generisanje reči za sortiranje.')
        log.info('Zavrseno generisanje reci za sortiranje.')
