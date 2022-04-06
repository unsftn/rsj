import gzip
import os
import pprint
from .models import Imenica, Glagol, Pridev, OblikGlagola, VarijantaImenice, VidPrideva
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
                wikimorph_update_noun(lema, oblik, podvrsta, padez, broj, rod)
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
            elif vrsta == 'Adv':  # prilozi
                pass
            elif vrsta == 'P':  # zamenice
                pass
            elif vrsta == 'Num':  # brojevi
                pass
            elif vrsta == 'C':  # veznici
                pass
            elif vrsta == 'I':  # uzvici
                pass
            elif vrsta == 'Part':  # recce
                pass
            elif vrsta == 'Prep':  # predlozi
                pass
            else:
                print(f'Nepoznata vrsta: {line}')
        except (ValueError, IndexError):
            print(f'Greska u parsiranju linije: {line}')
    infile.close()
    print(f'Ukupno parsirano {line_count} linija.')
    print(f'Dodavanje {len(imenice)} imenica...')
    save_nouns()
    print(f'Dodavanje {len(glagoli)} glagola...')
    save_verbs()
    print(f'Dodavanje {len(pridevi)} prideva...')
    save_adjectives()


def wikimorph_update_noun(lema, oblik, podvrsta, padez, broj, rod):
    try:
        imenica = imenice[lema]
    except KeyError:
        imenica = {'nomsg': lema, 'gensg': None, 'datsg': None, 'accsg': None, 'vocsg': None, 'inssg': None, 'locsg': None,
                   'nompl': None, 'genpl': None, 'datpl': None, 'accpl': None, 'vocpl': None, 'inspl': None, 'locpl': None,
                   'varijante': []}
        imenice[lema] = imenica
    search_list = [imenica] + imenica['varijante']
    found_slot = False
    for item in search_list:
        if item[padez+broj] == oblik:
            found_slot = True
            break
        if not item[padez+broj] and item[padez+broj] != oblik:
            item[padez+broj] = oblik
            found_slot = True
            break
    if not found_slot:
        nova_varijanta = {'nomsg': None, 'gensg': None, 'datsg': None, 'accsg': None, 'vocsg': None, 'inssg': None, 'locsg': None,
                          'nompl': None, 'genpl': None, 'datpl': None, 'accpl': None, 'vocpl': None, 'inspl': None, 'locpl': None}
        nova_varijanta[padez + broj] = oblik
        imenica['varijante'].append(nova_varijanta)


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
    try:
        pridev = pridevi[lema]
    except KeyError:
        pridev = {'lema': lema, 'odredjeni': _make_adjective(), 'neodredjeni': _make_adjective(),
                  'komparativ': _make_adjective(), 'superlativ': _make_adjective()}
        pridevi[lema] = pridev
    vid = 'odredjeni'
    if podvrsta == 'indef':
        vid = 'neodredjeni'
    elif stepen == 'comp':
        vid = 'komparativ'
    elif stepen == 'sup':
        vid = 'superlativ'
    pridev[vid][rod + padez + broj] = oblik


def save_nouns():
    for nomjed, im in imenice.items():
        try:
            imenica = Imenica.objects.get(nomjed=nomjed)
        except Imenica.DoesNotExist:
            imenica = Imenica()
            imenica.nomjed = nomjed
        imenica.genjed = im['gensg']
        imenica.datjed = im['datsg']
        imenica.akujed = im['accsg']
        imenica.vokjed = im['vocsg']
        imenica.insjed = im['inssg']
        imenica.lokjed = im['locsg']
        imenica.nommno = im['nompl']
        imenica.genmno = im['genpl']
        imenica.datmno = im['datpl']
        imenica.akumno = im['accpl']
        imenica.vokmno = im['vocpl']
        imenica.insmno = im['inspl']
        imenica.lokmno = im['locpl']
        imenica.skip_indexing = True
        imenica.save()
        imenica.varijantaimenice_set.all().delete()
        for index, var in enumerate(im['varijante']):
            vi = VarijantaImenice.objects.create(imenica=imenica, redni_broj=index+1)
            vi.nomjed = var['nomsg']
            vi.genjed = var['gensg']
            vi.datjed = var['datsg']
            vi.akujed = var['accsg']
            vi.vokjed = var['vocsg']
            vi.insjed = var['inssg']
            vi.lokjed = var['locsg']
            vi.nommno = var['nompl']
            vi.genmno = var['genpl']
            vi.datmno = var['datpl']
            vi.akumno = var['accpl']
            vi.vokmno = var['vocpl']
            vi.insmno = var['inspl']
            vi.lokmno = var['locpl']
            vi.skip_indexing = True
            vi.save()


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


def save_adjectives():
    for lema, pr in pridevi.items():
        try:
            pridev = Pridev.objects.get(lema=lema)
            VidPrideva.objects.filter(pridev=pridev).delete()
        except Pridev.DoesNotExist:
            pridev = Pridev()
            pridev.lema = lema
            pridev.skip_indexing = True
            pridev.save()
        _save_vid_prideva(pridev, 1, pr['odredjeni'])
        _save_vid_prideva(pridev, 2, pr['neodredjeni'])
        _save_vid_prideva(pridev, 3, pr['komparativ'])
        _save_vid_prideva(pridev, 4, pr['superlativ'])


def _make_adjective():
    return {
        'mnomsg': None, 'mgensg': None, 'mdatsg': None, 'maccsg': None, 'mvocsg': None, 'minssg': None, 'mlocsg': None,
        'mnompl': None, 'mgenpl': None, 'mdatpl': None, 'maccpl': None, 'mvocpl': None, 'minspl': None, 'mlocpl': None,
        'fnomsg': None, 'fgensg': None, 'fdatsg': None, 'faccsg': None, 'fvocsg': None, 'finssg': None, 'flocsg': None,
        'fnompl': None, 'fgenpl': None, 'fdatpl': None, 'faccpl': None, 'fvocpl': None, 'finspl': None, 'flocpl': None,
        'nnomsg': None, 'ngensg': None, 'ndatsg': None, 'naccsg': None, 'nvocsg': None, 'ninssg': None, 'nlocsg': None,
        'nnompl': None, 'ngenpl': None, 'ndatpl': None, 'naccpl': None, 'nvocpl': None, 'ninspl': None, 'nlocpl': None,
    }


def _is_empty_adjective(adj):
    return all(v is None for v in list(adj.values()))


def _save_vid_prideva(pridev, vid, obj):
    if not _is_empty_adjective(obj):
        VidPrideva.objects.create(
            pridev=pridev, vid=vid,
            mnomjed=obj['mnomsg'], mgenjed=obj['mgensg'], mdatjed=obj['mdatsg'], makujed=obj['maccsg'], mvokjed=obj['mvocsg'], minsjed=obj['minssg'], mlokjed=obj['mlocsg'],
            mnommno=obj['mnompl'], mgenmno=obj['mgenpl'], mdatmno=obj['mdatpl'], makumno=obj['maccpl'], mvokmno=obj['mvocpl'], minsmno=obj['minspl'], mlokmno=obj['mlocpl'],
            znomjed=obj['fnomsg'], zgenjed=obj['fgensg'], zdatjed=obj['fdatsg'], zakujed=obj['faccsg'], zvokjed=obj['fvocsg'], zinsjed=obj['finssg'], zlokjed=obj['flocsg'],
            znommno=obj['fnompl'], zgenmno=obj['fgenpl'], zdatmno=obj['fdatpl'], zakumno=obj['faccpl'], zvokmno=obj['fvocpl'], zinsmno=obj['finspl'], zlokmno=obj['flocpl'],
            snomjed=obj['nnomsg'], sgenjed=obj['ngensg'], sdatjed=obj['ndatsg'], sakujed=obj['naccsg'], svokjed=obj['nvocsg'], sinsjed=obj['ninssg'], slokjed=obj['nlocsg'],
            snommno=obj['nnompl'], sgenmno=obj['ngenpl'], sdatmno=obj['ndatpl'], sakumno=obj['naccpl'], svokmno=obj['nvocpl'], sinsmno=obj['ninspl'], slokmno=obj['nlocpl'],
        )


def ___wikimorph_update_noun2(lema, oblik, podvrsta, padez, broj, rod):
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


