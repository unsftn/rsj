from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from ...models import *

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Assign words with no owner to the given user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email of user who will become owner of words with no owner')

    def handle(self, *args, **options):
        start_time = datetime.now()
        email = options.get('email')
        try:
            user = UserProxy.objects.get(email=email)
            ukupno = 0
            for vrsta_reci in [Imenica, Glagol, Pridev, Zamenica, Prilog, Recca, Broj, Predlog, Uzvik, Veznik]:
                ukupno += vrsta_reci.objects.filter(vlasnik__isnull=True).update(vlasnik=user)
            log.info(f'Korisniku {email} dodeljeno ukupno {ukupno} reci')
        except UserProxy.DoesNotExist:
            log.info(f'Korisnik {email} nije pronadjen')
        end_time = datetime.now()
        log.info(f'Obrada trajala {str(end_time-start_time)}')
