import logging
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from odrednice.models import Kvalifikator

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Copy coders (e.g. qualifiers) to in-memory database'

    def handle(self, *args, **options):
        try:
            kvalifikatori = Kvalifikator.objects.using('default').all()
            for k in kvalifikatori:
                k.save(using='memory')
            self.stdout.write(self.style.SUCCESS('Kopirani kvalifikatori u in-memory bazu'))
        except OperationalError:
            pass