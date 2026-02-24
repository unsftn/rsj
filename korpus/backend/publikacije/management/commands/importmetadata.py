from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from publikacije.models import *
from publikacije.cyrlat import lat_to_cyr, cyr_to_lat
from publikacije.googlesheets import authorize, read_range

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import publication metadata from the Google sheet'

    def handle(self, *args, **options):
        start_time = datetime.now()
        log.info(f'Autorizacija za Google Sheets...')
        credentials = authorize()
        log.info(f'Citanje iz Google Sheets...')
        results = read_range(credentials, settings.KORPUS_SPREADSHEET_ID, 'Korpus!A3:Q5000')
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
        if len(row) < 17:
            row.extend([''] * (17 - len(row)))
        pub = find_pub(row[1], row[4], bool(row[13]))
        if not pub:
            pub = insert_pub(row)
        else:
            update_pub(pub, row)
        count += 1
        if count > 0 and count % 1000 == 0:
            log.info(f'Uneto {count} publikacija...')
    log.info(f'Ukupno uneto {count} publikacija.')


def find_pub(title: str, year: str, cirilica: bool) -> Publikacija | None:
    year = clean_year(year)
    naslov1 = title.strip()
    naslov2 = lat_to_cyr(naslov1) if cirilica else cyr_to_lat(naslov1)
    pub1 = Publikacija.objects.filter(naslov=title, godina=year).first()
    if pub1:
        return pub1
    pub2 = Publikacija.objects.filter(naslov=naslov2, godina=year).first()
    if pub2:
        return pub2
    return None


def update_pub(pub: Publikacija, row: list) -> None:
    # reset_autor(pub, row[0])
    cirilica = bool(row[13])
    naslov = lat_to_cyr(row[1].strip()) if cirilica else cyr_to_lat(row[1].strip())
    prevodilac = lat_to_cyr(row[3].strip()) if cirilica else cyr_to_lat(row[3].strip())
    pub.naslov = naslov
    pub.skracenica = lat_to_cyr(row[2].strip())
    pub.prevodilac = prevodilac
    pub.prvo_izdanje = clean_year(row[5])
    pub.napomena = row[10].strip()
    pub.zanr = row[11].strip()
    pub.tom = row[15].strip()
    pub.izdavac = row[16].strip()
    reset_autor(pub, row[0], cirilica)
    pub.save()


def insert_pub(row: list) -> Publikacija:
    godina = clean_year(row[4])
    cirilica = bool(row[13])
    naslov = lat_to_cyr(row[1].strip()) if cirilica else cyr_to_lat(row[1].strip())
    pub = Publikacija.objects.create(
        naslov=naslov,
        godina=godina,
        prevodilac=row[3].strip(),
        prvo_izdanje=clean_year(row[5]),
        napomena=row[10].strip(),
        zanr=row[11].strip(),
        tom=row[15].strip(),
        izdavac=row[16].strip(),
        user_id=1,
        skracenica=lat_to_cyr(row[2].strip()))
    reset_autor(pub, row[0], cirilica)
    return pub


def clean_year(year: str) -> str:
    year = year.strip()
    if year.endswith('.'):
        year = year[:-1]
    return year


def reset_autor(pub: Publikacija, autor: str, cirilica: bool) -> None:
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
    if cirilica:
        ime = lat_to_cyr(ime)
        prezime = lat_to_cyr(prezime)
    Autor.objects.create(publikacija=pub, redni_broj=1, ime=ime, prezime=prezime)
