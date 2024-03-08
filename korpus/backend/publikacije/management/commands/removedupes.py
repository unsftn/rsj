import logging
from django.core.management.base import BaseCommand, CommandError
from publikacije.models import Publikacija, TekstPublikacije, Potkorpus

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Remove duplicate publications from corpus'

    def add_arguments(self, parser):
        parser.add_argument('sub_id', type=int, help='Subcorpus ID')

    def handle(self, *args, **options):
        sub_id = options.get('sub_id')
        try:
            pk = Potkorpus.objects.get(id=sub_id)
            log.info(f'Subcorpus: {pk.id} - {pk.naziv}')
        except Potkorpus.DoesNotExist:
            raise CommandError(f'Subcorpus with ID {sub_id} does not exist')
        titles = {}
        for_removal = []
        total = 0
        try:
            pubs = Publikacija.objects.filter(potkorpus=sub_id)
            for pub in pubs:
                total += 1
                key = nvl(pub.godina, '----') + ':' + pub.naslov
                if key in titles:
                    for_removal.append(pub)
                else:
                    titles[key] = pub
            log.info(f'Found {len(for_removal)} duplicates out of {total} publications.')
            for pub in for_removal:
                TekstPublikacije.objects.filter(publikacija=pub).delete()    
                pub.delete()
            self.stdout.write(f'Successfully removed duplicates.')
        except Exception as ex:
            log.fatal(ex)


def nvl(value, default):
    return value if value else default
