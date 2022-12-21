from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from publikacije.models import *
from publikacije.googlesheets import authorize, read_range

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import publication metadata from the Google sheet'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info(f'Autorizacija za Google Sheets...')
        credentials = authorize()
        log.info(f'Citanje iz Google Sheets...')
        results = read_range(credentials, settings.KORPUS_SPREADSHEET_ID, 'Korpus!A3:L5000')
        log.info('Azuriranje baze...')
        update_metadata(results)
        end_time = datetime.now()
        log.info(f'Import metapodataka trajao ukupno {str(end_time-start_time)}')


def update_metadata(results: list) -> None:
    count = 0
    for row in results:
        # preskoci ako nema naslova
        if not row[1]:
            continue
        if len(row) < 12:
            row.extend([''] * (12 - len(row)))
        pub = find_pub(row[1], row[4])
        if not pub:
            pub = insert_pub(row)
        else:
            update_pub(pub, row)
        count += 1
        if count > 0 and count % 1000 == 0:
            log.info(f'Uneto {count} publikacija...')
    log.info(f'Ukupno uneto {count} publikacija.')


def find_pub(title: str, year: str) -> Publikacija:
    year = clean_year(year)
    try:
        return Publikacija.objects.get(naslov=title, godina=year)
    except Publikacija.DoesNotExist:
        return None


def update_pub(pub: Publikacija, row: list) -> None:
    # reset_autor(pub, row[0])
    pub.skracenica = row[2].strip()
    pub.prevodilac = row[3].strip()
    pub.prvo_izdanje = clean_year(row[5])
    pub.napomena = row[10].strip()
    pub.zanr = row[11].strip()
    pub.save()
    

def insert_pub(row: list) -> Publikacija:
    godina = clean_year(row[4])    
    pub = Publikacija.objects.create(
        naslov=row[1].strip(), 
        godina=godina,
        prevodilac=row[3].strip(),
        prvo_izdanje=clean_year(row[5]),
        napomena=row[10].strip(),
        zanr=row[11].strip(),
        user_id=1, 
        skracenica=row[2].strip())
    reset_autor(pub, row[0])
    return pub


def clean_year(year: str) -> str:
    year = year.strip()
    if year.endswith('.'):
        year = year[:-1]
    return year


def reset_autor(pub: Publikacija, autor: str) -> None:
    pub.autor_set.all().delete()
    autor = autor.strip()
    if not autor:
        return
    if autor.endswith('.'):
        autor = autor[:-1]
    if autor.endswith('i dr'):
        autor = autor[:-4]
    
    ime_prezime = autor.split()
    if len(ime_prezime) == 1:
        prezime = ''
        ime = ime_prezime[0]
    elif len(ime_prezime) == 2:
        prezime = ime_prezime[0]
        ime = ime_prezime[1]
    elif len(ime_prezime) == 3:
        prezime = ime_prezime[0] + ' ' + ime_prezime[1]
        ime = ime_prezime[2]
    else:
        prezime = ime_prezime[0] + ' ' + ime_prezime[1]
        ime = ime_prezime[2] + ' ' + ime_prezime[3]
    Autor.objects.create(publikacija=pub, redni_broj=1, ime=ime, prezime=prezime)
