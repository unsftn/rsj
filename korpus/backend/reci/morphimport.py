import gzip
import os
from .models import Imenica, Glagol, Pridev, OblikGlagola, VarijantaImenice
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
        pridev = {'lema': lema}
        pridevi[lema] = pridev
    if rod == 'm':
        vid = 'o'
        if podvrsta == 'indef':
            vid = 'n'
    else:
        vid = 'p'
    if stepen == 'comp':
        vid = 'k'
    elif stepen == 'sup':
        vid = 's'
    rod = 'z' if rod == 'f' else rod
    rod = 's' if rod == 'n' else rod
    padez = 'aku' if padez == 'acc' else padez
    padez = 'vok' if padez == 'voc' else padez
    padez = 'lok' if padez == 'loc' else padez
    broj = 'jed' if broj == 'sg' else broj
    broj = 'mno' if broj == 'pl' else broj
    pridev[rod + vid + padez + broj] = oblik


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
        except Pridev.DoesNotExist:
            pridev = Pridev()
            pridev.lema = lema
        pridev.skip_indexing = True
        pridev.monomjed = pr.get('monomjed')
        pridev.mogenjed = pr.get('mogenjed')
        pridev.modatjed = pr.get('modatjed')
        pridev.moakujed = pr.get('moakujed')
        pridev.movokjed = pr.get('movokjed')
        pridev.moinsjed = pr.get('moinsjed')
        pridev.molokjed = pr.get('molokjed')
        pridev.monommno = pr.get('monommno')
        pridev.mogenmno = pr.get('mogenmno')
        pridev.modatmno = pr.get('modatmno')
        pridev.moakumno = pr.get('moakumno')
        pridev.movokmno = pr.get('movokmno')
        pridev.moinsmno = pr.get('moinsmno')
        pridev.molokmno = pr.get('molokmno')
        pridev.mnnomjed = pr.get('mnnomjed')
        pridev.mngenjed = pr.get('mngenjed')
        pridev.mndatjed = pr.get('mndatjed')
        pridev.mnakujed = pr.get('mnakujed')
        pridev.mnvokjed = pr.get('mnvokjed')
        pridev.mninsjed = pr.get('mninsjed')
        pridev.mnlokjed = pr.get('mnlokjed')
        pridev.mnnommno = pr.get('mnnommno')
        pridev.mngenmno = pr.get('mngenmno')
        pridev.mndatmno = pr.get('mndatmno')
        pridev.mnakumno = pr.get('mnakumno')
        pridev.mnvokmno = pr.get('mnvokmno')
        pridev.mninsmno = pr.get('mninsmno')
        pridev.mnlokmno = pr.get('mnlokmno')
        pridev.mknomjed = pr.get('mknomjed')
        pridev.mkgenjed = pr.get('mkgenjed')
        pridev.mkdatjed = pr.get('mkdatjed')
        pridev.mkakujed = pr.get('mkakujed')
        pridev.mkvokjed = pr.get('mkvokjed')
        pridev.mkinsjed = pr.get('mkinsjed')
        pridev.mklokjed = pr.get('mklokjed')
        pridev.mknommno = pr.get('mknommno')
        pridev.mkgenmno = pr.get('mkgenmno')
        pridev.mkdatmno = pr.get('mkdatmno')
        pridev.mkakumno = pr.get('mkakumno')
        pridev.mkvokmno = pr.get('mkvokmno')
        pridev.mkinsmno = pr.get('mkinsmno')
        pridev.mklokmno = pr.get('mklokmno')
        pridev.msnomjed = pr.get('msnomjed')
        pridev.msgenjed = pr.get('msgenjed')
        pridev.msdatjed = pr.get('msdatjed')
        pridev.msakujed = pr.get('msakujed')
        pridev.msvokjed = pr.get('msvokjed')
        pridev.msinsjed = pr.get('msinsjed')
        pridev.mslokjed = pr.get('mslokjed')
        pridev.msnommno = pr.get('msnommno')
        pridev.msgenmno = pr.get('msgenmno')
        pridev.msdatmno = pr.get('msdatmno')
        pridev.msakumno = pr.get('msakumno')
        pridev.msvokmno = pr.get('msvokmno')
        pridev.msinsmno = pr.get('msinsmno')
        pridev.mslokmno = pr.get('mslokmno')
        pridev.zpnomjed = pr.get('zpnomjed')
        pridev.zpgenjed = pr.get('zpgenjed')
        pridev.zpdatjed = pr.get('zpdatjed')
        pridev.zpakujed = pr.get('zpakujed')
        pridev.zpvokjed = pr.get('zpvokjed')
        pridev.zpinsjed = pr.get('zpinsjed')
        pridev.zplokjed = pr.get('zplokjed')
        pridev.zpnommno = pr.get('zpnommno')
        pridev.zpgenmno = pr.get('zpgenmno')
        pridev.zpdatmno = pr.get('zpdatmno')
        pridev.zpakumno = pr.get('zpakumno')
        pridev.zpvokmno = pr.get('zpvokmno')
        pridev.zpinsmno = pr.get('zpinsmno')
        pridev.zplokmno = pr.get('zplokmno')
        pridev.zknomjed = pr.get('zknomjed')
        pridev.zkgenjed = pr.get('zkgenjed')
        pridev.zkdatjed = pr.get('zkdatjed')
        pridev.zkakujed = pr.get('zkakujed')
        pridev.zkvokjed = pr.get('zkvokjed')
        pridev.zkinsjed = pr.get('zkinsjed')
        pridev.zklokjed = pr.get('zklokjed')
        pridev.zknommno = pr.get('zknommno')
        pridev.zkgenmno = pr.get('zkgenmno')
        pridev.zkdatmno = pr.get('zkdatmno')
        pridev.zkakumno = pr.get('zkakumno')
        pridev.zkvokmno = pr.get('zkvokmno')
        pridev.zkinsmno = pr.get('zkinsmno')
        pridev.zklokmno = pr.get('zklokmno')
        pridev.zsnomjed = pr.get('zsnomjed')
        pridev.zsgenjed = pr.get('zsgenjed')
        pridev.zsdatjed = pr.get('zsdatjed')
        pridev.zsakujed = pr.get('zsakujed')
        pridev.zsvokjed = pr.get('zsvokjed')
        pridev.zsinsjed = pr.get('zsinsjed')
        pridev.zslokjed = pr.get('zslokjed')
        pridev.zsnommno = pr.get('zsnommno')
        pridev.zsgenmno = pr.get('zsgenmno')
        pridev.zsdatmno = pr.get('zsdatmno')
        pridev.zsakumno = pr.get('zsakumno')
        pridev.zsvokmno = pr.get('zsvokmno')
        pridev.zsinsmno = pr.get('zsinsmno')
        pridev.zslokmno = pr.get('zslokmno')
        pridev.spnomjed = pr.get('spnomjed')
        pridev.spgenjed = pr.get('spgenjed')
        pridev.spdatjed = pr.get('spdatjed')
        pridev.spakujed = pr.get('spakujed')
        pridev.spvokjed = pr.get('spvokjed')
        pridev.spinsjed = pr.get('spinsjed')
        pridev.splokjed = pr.get('splokjed')
        pridev.spnommno = pr.get('spnommno')
        pridev.spgenmno = pr.get('spgenmno')
        pridev.spdatmno = pr.get('spdatmno')
        pridev.spakumno = pr.get('spakumno')
        pridev.spvokmno = pr.get('spvokmno')
        pridev.spinsmno = pr.get('spinsmno')
        pridev.splokmno = pr.get('splokmno')
        pridev.sknomjed = pr.get('sknomjed')
        pridev.skgenjed = pr.get('skgenjed')
        pridev.skdatjed = pr.get('skdatjed')
        pridev.skakujed = pr.get('skakujed')
        pridev.skvokjed = pr.get('skvokjed')
        pridev.skinsjed = pr.get('skinsjed')
        pridev.sklokjed = pr.get('sklokjed')
        pridev.sknommno = pr.get('sknommno')
        pridev.skgenmno = pr.get('skgenmno')
        pridev.skdatmno = pr.get('skdatmno')
        pridev.skakumno = pr.get('skakumno')
        pridev.skvokmno = pr.get('skvokmno')
        pridev.skinsmno = pr.get('skinsmno')
        pridev.sklokmno = pr.get('sklokmno')
        pridev.ssnomjed = pr.get('ssnomjed')
        pridev.ssgenjed = pr.get('ssgenjed')
        pridev.ssdatjed = pr.get('ssdatjed')
        pridev.ssakujed = pr.get('ssakujed')
        pridev.ssvokjed = pr.get('ssvokjed')
        pridev.ssinsjed = pr.get('ssinsjed')
        pridev.sslokjed = pr.get('sslokjed')
        pridev.ssnommno = pr.get('ssnommno')
        pridev.ssgenmno = pr.get('ssgenmno')
        pridev.ssdatmno = pr.get('ssdatmno')
        pridev.ssakumno = pr.get('ssakumno')
        pridev.ssvokmno = pr.get('ssvokmno')
        pridev.ssinsmno = pr.get('ssinsmno')
        pridev.sslokmno = pr.get('sslokmno')
        pridev.save()


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


