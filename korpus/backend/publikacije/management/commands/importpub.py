import logging
import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Max
from publikacije.models import Publikacija, TekstPublikacije
from publikacije.processing import OPERATION_DEFINITIONS, clean_pdf_file

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import text for publication'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Print output to console')
        parser.add_argument('pub_id', type=int, help='Publication ID')
        parser.add_argument('file', type=str, help='File to import')
        parser.add_argument('ops', nargs='+', help='Operations')

    def handle(self, *args, **options):
        pub_id = options.get('pub_id')
        input_file = options.get('file')
        dry_run = options['dry_run']
        ops = options.get('ops')
        operations = []
        opdef = None
        expected_params = 0
        current_param_run = []
        for arg in ops:
            if len(current_param_run) < expected_params:
                current_param_run.append(arg)
                continue
            opdef = OPERATION_DEFINITIONS.get(int(arg))
            if opdef:
                expected_params = len(opdef['params'])
                current_param_run = []
                operations.append({'opcode': int(arg), 'params': current_param_run})
            else:
                raise CommandError(f'Operation with ID {arg} does not exist')
        try:
            Publikacija.objects.get(id=pub_id)
        except Publikacija.DoesNotExist:
            raise CommandError(f'Publication with ID {pub_id} does not exist')
        if not os.path.isfile(input_file):
            raise CommandError(f'Input file {input_file} does not exist')
        self.stdout.write(f'Publication ID: {pub_id}')
        self.stdout.write(f'Input file: {input_file}')
        self.stdout.write(f'Operations:')
        for op in operations:
            params = ' '.join(['"'+param+'"' for param in op['params']])
            self.stdout.write(f'  {OPERATION_DEFINITIONS[op["opcode"]]["description"]}: {params}')
        self.stdout.write(f'Dry run: {dry_run}')
        pages = clean_pdf_file(input_file, operations)
        if dry_run:
            for page in pages:
                self.stdout.write('===')
                self.stdout.write(page)
        else:
            prethodni = TekstPublikacije.objects.filter(publikacija_id=pub_id).aggregate(Max('redni_broj'))['redni_broj__max'] or 0
            for index, page in enumerate(pages):
                TekstPublikacije.objects.create(publikacija_id=pub_id, redni_broj=prethodni+index+1, tekst=page)
            self.stdout.write(f'Import finished, total number of pages: {len(pages)}')
