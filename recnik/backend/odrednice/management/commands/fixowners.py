import logging
import unicodedata as ud
from django.core.management.base import BaseCommand
from odrednice.models import Odrednica
from odrednice.text import remove_punctuation
from pretraga.cyrlat import lat_to_cyr

log = logging.getLogger(__name__)

cyrillic_letters = {}


class Command(BaseCommand):
    help = 'Fix ownership of Odrednica objects'

    def handle(self, *args, **options):
        self.style.NOTICE(f'Ispravke za reci koje su kod redaktora')
        log.info('Ispravke za reci koje su kod redaktora')

        count = 0
        odrednice = Odrednica.objects.filter(stanje=2)
        for odr in odrednice:
            poslednja_predaja = odr.izmenaodrednice_set.filter(operacija_izmene=4).latest('vreme')
            odr.obradjivac = poslednja_predaja.user
            poslednja_izmena = odr.izmenaodrednice_set.latest('vreme')
            if poslednja_izmena.id != poslednja_predaja.id:
                odr.redaktor = poslednja_izmena.user
                count += 1
                self.style.NOTICE(f'Izmenjen redaktor u {odr.rec}')
                log.info(f'Izmenjen redaktor u {odr.rec}')
                odr.save()
            
        self.style.SUCCESS(f'Izmenjen redaktor u {count} odrednica.')
        log.info(f'Izmenjen redaktor u {count} odrednica.')
