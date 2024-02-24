import json
import logging
import os
import re
from django.core.management.base import BaseCommand, CommandError
from publikacije.models import Publikacija, TekstPublikacije, Autor
from publikacije.processing import init_tags

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import publications from line-by-line JSON file'

    def add_arguments(self, parser):
        parser.add_argument('subcorpus_id', type=int, help='Subcorpus ID')
        parser.add_argument('user_id', type=int, help='User ID')
        parser.add_argument('file', type=str, help='File to import')
        parser.add_argument('--dry-run', action='store_true', help='Print output to console')

    def handle(self, *args, **options):
        input_file = options.get('file')
        subcorpus_id = options.get('subcorpus_id')
        user_id = options.get('user_id')
        dry_run = options['dry_run']
        if not os.path.isfile(input_file):
            raise CommandError(f'Input file {input_file} does not exist')
        self.stdout.write(f'Subcorpus ID: {subcorpus_id}')
        self.stdout.write(f'User ID: {user_id}')
        self.stdout.write(f'Input file: {input_file}')
        self.stdout.write(f'Dry run: {dry_run}')
        count = 0
        with open(input_file, 'r') as infile:
            for line in infile.readlines():
                line = line.strip()
                if not line:
                    continue
                tp = self.save_article(line, subcorpus_id, user_id)
                if tp:
                    count += 1
                if count > 0 and count % 1000 == 0:
                    self.stdout.write(f'Imported {count} articles')
                    self.stdout.flush()
        log.info(f'Imported total of {count} articles.')

    def save_article(self, line, subcorpus_id, user_id):
        try:
            obj = json.loads(line)
            naslov = obj.get('title') or obj.get('naslov')
            izdavac = obj.get('publisher') or obj.get('izdavac') or obj.get('channel_title')
            godina = obj.get('year') or obj.get('godina')
            if godina and len(godina) > 10:
                try:
                    godina = re.search(r'\d{4}', godina).group(0)
                except Exception:
                    godina = godina[:10]
            broj = obj.get('number') or obj.get('broj')
            if broj:
                broj = broj[:10]
            url = obj.get('url')
            tekst = obj.get('body') or obj.get('text') or obj.get('tekst') or obj.get('content') or obj.get('transcription')
            if not tekst:
                return None
            tekst = tekst.strip()
            if not naslov:
                naslov = '---'

            pub = Publikacija.objects.create(naslov=naslov[:300], izdavac=izdavac, godina=godina, url=url, potkorpus_id=subcorpus_id, user_id=user_id, broj=broj)
            
            autor = obj.get('author') or obj.get('autor')
            if isinstance(autor, list):
                autor = autor[0]
            if autor:
                delovi = autor.split()
                if len(delovi) > 1:
                    ime, prezime = delovi[0][:50], delovi[1][:50]
                else:
                    prezime, ime = autor[:50], ''
                Autor.objects.create(publikacija=pub, redni_broj=1, ime=ime, prezime=prezime)
            
            tp = TekstPublikacije.objects.create(publikacija=pub, redni_broj=1, tekst=tekst, tagovan_tekst=init_tags(tekst))
            return tp
        except ValueError as ex:
            log.fatal(f'Could not parse: {line}')
            log.fatal(ex)
            return None
