import logging
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from odrednice.models import Odrednica, StatistikaUnosa, StavkaStatistikeUnosa
from render.renderer import count_printable_chars

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate stats for users'

    def handle(self, *args, **options):
        log.info('Generisanje statistike obradjivaca...')
        users = {}
        for odr in Odrednica.objects.all():
            length = count_printable_chars(odr)
            if odr.obradjivac:
                if odr.stanje == 1:
                    if users.get(odr.obradjivac.email):
                        users[odr.obradjivac.email]['broj_odrednica'] += 1
                        users[odr.obradjivac.email]['broj_znakova'] += length
                    else:
                        users[odr.obradjivac.email] = {
                            'id': odr.obradjivac.id,
                            'email': odr.obradjivac.email,
                            'first_name': odr.obradjivac.first_name,
                            'last_name': odr.obradjivac.last_name,
                            'broj_odrednica': 1,
                            'broj_znakova': length,
                            'zavrsenih_odrednica': 0,
                            'zavrsenih_znakova': 0
                        }
                else:
                    if users.get(odr.obradjivac.email):
                        users[odr.obradjivac.email]['zavrsenih_odrednica'] += 1
                        users[odr.obradjivac.email]['zavrsenih_znakova'] += length
                    else:
                        users[odr.obradjivac.email] = {
                            'id': odr.obradjivac.id,
                            'email': odr.obradjivac.email,
                            'first_name': odr.obradjivac.first_name,
                            'last_name': odr.obradjivac.last_name,
                            'broj_odrednica': 0,
                            'broj_znakova': 0,
                            'zavrsenih_odrednica': 1,
                            'zavrsenih_znakova': length
                        }

        sada = now()
        stat = StatistikaUnosa.objects.create(vreme=sada)
        for user in users.values():
            StavkaStatistikeUnosa.objects.create(
                statistika=stat,
                user_id=user['id'],
                broj_odrednica=user['broj_odrednica'],
                broj_znakova=user['broj_znakova'],
                zavrsenih_odrednica=user['zavrsenih_odrednica'],
                zavrsenih_znakova=user['zavrsenih_znakova']
            )
        self.style.SUCCESS(f'Uspesno generisana statistika ID: {stat.id}')
        log.info('Generisanje statistike obradjivaca zavrseno.')
