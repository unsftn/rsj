import gzip
import os
import pprint
from .models import Imenica, Glagol, Pridev, OblikGlagola
from .cyrlat import lat_to_cyr

imenice = {}
glagoli = {}
pridevi = {}


MAPA_VREMENA = {
    'pres': 1,
    'fut': 2,
    'aor': 3,
    'impf': 4,
    'imper': 5
}


def wikimorph_import(filename, gzipped=False):
    """
    Importuje wikimorph-sr fajl u bazu podataka.

    Vise informacija o fajlu je ovde:
    http://parcolab.univ-tlse2.fr/en/about/resources/
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)
    global imenice, glagoli, pridevi
    imenice = {}
    glagoli = {}
    pridevi = {}
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
                # wikimorph_update_noun(lema, oblik, podvrsta, padez, broj, rod)
            elif vrsta == 'V':
                podvrsta = delovi_opisa[1]
                vreme = delovi_opisa[2]
                lice = delovi_opisa[3]
                broj = delovi_opisa[4]
                rod = delovi_opisa[5]
                negacija = delovi_opisa[6]
                wikimorph_update_verb(lema, oblik, podvrsta, vreme, lice, broj, rod, negacija)
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
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(glagoli[list(glagoli.keys())[20]])
    save_verbs()


def wikimorph_update_noun(lema, oblik, podvrsta, padez, broj, rod):
    try:
        imenica = Imenica.objects.get(nomjed=lema)
    except Imenica.DoesNotExist:
        imenica = Imenica()
        imenica.nomjed = lema
    # TODO podvrsta
    # TODO varijante
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


def wikimorph_update_verb(lema, oblik, podvrsta, vreme, lice, broj, rod, negacija):
    try:
        glagol = glagoli[lema]
    except KeyError:
        glagol = {'infinitiv': lema, 'vremena': {}}
        glagoli[lema] = glagol
    try:
        glvr = glagol['vremena'][vreme]
    except KeyError:
        glvr = {'vreme': vreme, 'oblici': []}
        glagol['vremena'][vreme] = glvr
    glvr['oblici'].append({'lice': lice, 'broj': broj, 'rod': rod, 'negacija': negacija, 'oblik': oblik,})


def wikimorph_update_adjective(lema, oblik, podvrsta, padez, rod, broj, stepen):
    pass


def save_verbs():
    for infinitiv, glagol in glagoli.items():
        try:
            gl = Glagol.objects.get(infinitiv=infinitiv)
        except Glagol.DoesNotExist:
            gl = Glagol()
            gl.infinitiv = infinitiv
            gl.skip_indexing = True
            gl.save()
        for sifra_vremena, vr in glagol['vremena'].items():
            vrcode = MAPA_VREMENA.get(sifra_vremena)
            if vrcode:
                try:
                    og = OblikGlagola.objects.get(glagol=gl, vreme=vrcode)
                except OblikGlagola.DoesNotExist:
                    og = OblikGlagola.objects.create(glagol=gl, vreme=vrcode)
                for oblik in vr['oblici']:
                    broj = oblik['broj']
                    lice = oblik['lice']
                    tekst = oblik['oblik']
                    if broj == 'sg' and lice == '1':
                        og.jd1 = tekst
                    elif broj == 'sg' and lice == '2':
                        og.jd2 = tekst
                    elif broj == 'sg' and lice == '3':
                        og.jd3 = tekst
                    if broj == 'pl' and lice == '1':
                        og.mn1 = tekst
                    elif broj == 'pl' and lice == '2':
                        og.mn2 = tekst
                    elif broj == 'pl' and lice == '3':
                        og.mn3 = tekst
                og.save()
            elif sifra_vremena == 'partact':  # radni glagolski pridev
                for oblik in vr['oblici']:
                    broj = oblik['broj']
                    rod = oblik['rod']
                    tekst = oblik['oblik']
                    if broj == 'sg' and rod == 'm':
                        gl.rgp_mj = tekst
                    elif broj == 'sg' and rod == 'f':
                        gl.rgp_zj = tekst
                    elif broj == 'sg' and rod == 'n':
                        gl.rgp_sj = tekst
                    elif broj == 'pl' and rod == 'm':
                        gl.rgp_mm = tekst
                    elif broj == 'pl' and rod == 'f':
                        gl.rgp_zm = tekst
                    elif broj == 'pl' and rod == 'n':
                        gl.rgp_sm = tekst
            elif sifra_vremena == 'partpass':  # trpni glagolski pridev
                for oblik in vr['oblici']:
                    broj = oblik['broj']
                    rod = oblik['rod']
                    tekst = oblik['oblik']
                    if broj == 'sg' and rod == 'm':
                        gl.tgp_mj = tekst
                    elif broj == 'sg' and rod == 'f':
                        gl.tgp_zj = tekst
                    elif broj == 'sg' and rod == 'n':
                        gl.tgp_sj = tekst
                    elif broj == 'pl' and rod == 'm':
                        gl.tgp_mm = tekst
                    elif broj == 'pl' and rod == 'f':
                        gl.tgp_zm = tekst
                    elif broj == 'pl' and rod == 'n':
                        gl.tgp_sm = tekst
            elif sifra_vremena == 'partpres':  # glagolski prilog sadasnji
                gl.gps = vr['oblici'][0]['oblik']
            elif sifra_vremena == 'partpast':  # glagolski prilog prosli
                gl.gpp = vr['oblici'][0]['oblik']
        gl.skip_indexing = True
        gl.save()
