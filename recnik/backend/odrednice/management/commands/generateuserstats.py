from datetime import datetime
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
        start_time = datetime.now()
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
            else:
                if users.get('0000'):
                    users['0000']['broj_odrednica'] += 1
                    users['0000']['broj_znakova'] += length
                else:
                    users['0000'] = {
                        'id': None,
                        'email': '0000@rsj.rs',
                        'first_name': 'Није',
                        'last_name': 'преузето',
                        'broj_odrednica': 1,
                        'broj_znakova': length,
                        'zavrsenih_odrednica': 0,
                        'zavrsenih_znakova': 0
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
        log.info('Generisanje statistike obradjivaca zavrseno.')
        end_time = datetime.now()
        log.info(f'Generisanje trajalo ukupno {str(end_time-start_time)}')
