from itertools import chain
from django.core.management.base import BaseCommand
from django.conf import settings
from publikacije.models import Publikacija, FajlPublikacije


class Command(BaseCommand):
    help = 'Extract text from a PDF or Word file(s)'

    def add_arguments(self, parser):
        parser.add_argument('file_ids', nargs='?', type=str)

    def handle(self, *args, **options):
        ranges = options['file_ids']
        ids = parse_range_list(ranges)
        self.stdout.write(self.style.SUCCESS(ids))
        publikacije = Publikacija.objects.filter(pk__in=ids)
        for pub in publikacije:
            self.stdout.write(f'Parsing publication {pub.id}: {pub.title}...')
            for pub_file in pub.fajlpublikacije_set.all():
                self.stdout.write(f'Parsing file {pub_file.uploaded_file}... ', ending='')
                # TODO: invoke parser here
                self.stdout.write(self.style.SUCCESS('done.'))


def parse_range(rng):
    parts = rng.split('-')
    if 1 > len(parts) > 2:
        raise ValueError("Bad range: '%s'" % (rng,))
    parts = [int(i) for i in parts]
    start = parts[0]
    end = start if len(parts) == 1 else parts[1]
    if start > end:
        end, start = start, end
    return range(start, end + 1)


def parse_range_list(rngs):
    return sorted(set(chain(*[parse_range(rng) for rng in rngs.split(',')])))

