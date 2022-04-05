import gzip
import os
from .models import Imenica, Glagol, Pridev
from .cyrlat import lat_to_cyr


def wikimorph_import(filename, gzipped=False):
    """
    Importuje wikimorph-sr fajl u bazu podataka.

    Vise informacija o fajlu je ovde:
    http://parcolab.univ-tlse2.fr/en/about/resources/
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)
    infile = gzip.open(filename, 'rt', encoding='utf-8') if gzipped else open(filename, 'r')
    line_count = 0
    for line in infile.readlines():
        line_count += 1
        if line_count % 100000 == 0:
            print(f'Parsirano linija: {line_count}')
        line = line.strip()
        if len(line) == 0:
            continue
        try:
            oblik, lema, opis = line.split()
            oblik = lat_to_cyr(oblik).lower()
            lema = lat_to_cyr(lema).lower()
            delovi_opisa = opis.split('_')
            vrsta = delovi_opisa[0]
            if vrsta == 'N':
                podvrsta = delovi_opisa[1]
                padez = delovi_opisa[2]
                broj = delovi_opisa[3]
                rod = delovi_opisa[4]
                wikimorph_update_noun(lema, oblik, podvrsta, padez, broj, rod)
            elif vrsta == 'V':
                podvrsta = delovi_opisa[1]
                vreme = delovi_opisa[2]
                lice = delovi_opisa[3]
                broj = delovi_opisa[4]
                negacija = delovi_opisa[5]
                wikimorph_update_verb(lema, oblik, podvrsta, vreme, lice, broj, negacija)
            elif vrsta == 'A':
                podvrsta = delovi_opisa[1]
                padez = delovi_opisa[2]
                broj = delovi_opisa[3]
                rod = delovi_opisa[4]
                stepen = delovi_opisa[5]
                wikimorph_update_adjective(lema, oblik, podvrsta, padez, rod, broj, stepen)
            else:
                # print(f'Nepoznata vrsta: {line}')
                pass
        except (ValueError, IndexError):
            print(f'Greska u parsiranju linije: {line}')
            continue
    infile.close()


def wikimorph_update_noun(lema, oblik, podvrsta, padez, broj, rod):
    try:
        imenica = Imenica.objects.get(nomjed=lema)
    except Imenica.DoesNotExist:
        imenica = Imenica()
        imenica.nomjed = lema
    # TODO podvrsta
    if padez == 'nom' and broj == 'sg':
        pass
    elif padez == 'gen' and broj == 'sg':
        imenica.genjed = oblik
    elif padez == 'dat' and broj == 'sg':
        imenica.datjed = oblik
    elif padez == 'acc' and broj == 'sg':
        imenica.akujed = oblik
    elif padez == 'voc' and broj == 'sg':
        imenica.vokjed = oblik
    elif padez == 'ins' and broj == 'sg':
        imenica.insjed = oblik
    elif padez == 'loc' and broj == 'sg':
        imenica.lokjed = oblik
    elif padez == 'nom' and broj == 'pl':
        imenica.nommno = oblik
    elif padez == 'gen' and broj == 'pl':
        imenica.genmno = oblik
    elif padez == 'dat' and broj == 'pl':
        imenica.datmno = oblik
    elif padez == 'acc' and broj == 'pl':
        imenica.akumno = oblik
    elif padez == 'voc' and broj == 'pl':
        imenica.vokmno = oblik
    elif padez == 'ins' and broj == 'pl':
        imenica.insmno = oblik
    elif padez == 'loc' and broj == 'pl':
        imenica.lokmno = oblik
    imenica.skip_indexing = True
    imenica.save()


def wikimorph_update_verb(lema, oblik, podvrsta, vreme, lice, broj, negacija):
    pass


def wikimorph_update_adjective(lema, oblik, podvrsta, padez, rod, broj, stepen):
    pass
