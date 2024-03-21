from datetime import datetime
from elasticsearch import NotFoundError
from publikacije.models import *
from .utils import *
from .cyrlat import *


def index_publikacija(pub_id, client=None):
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
    except Publikacija.DoesNotExist as ex:
        log.fatal(ex)
        return False

    for tp in publikacija.tekstpublikacije_set.all().order_by('redni_broj'):
        document = {
            'pk': publikacija.id,
            'potkorpus': publikacija.potkorpus.naziv if publikacija.potkorpus else '',
            'skracenica': publikacija.skracenica,
            'opis': publikacija.opis(),
            'tekst': tp.tekst,
            'tekst_reversed': tp.tekst,
            'tekst_case_sensitive': tp.tekst,
            'tekst_whitespace': tp.tekst,
            'timestamp': datetime.now().isoformat()[:-3] + 'Z',
        }
        try:
            if not client:
                client = get_es_client()
            client.index(index=PUB_INDEX, id=tp.id, document=document)
        except Exception as ex:
            log.fatal(ex)
            return False
    return True


def index_naslov(pub_id, client=None):
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
    except Publikacija.DoesNotExist as ex:
        log.fatal(ex)
        return False

    opis = publikacija.opis()
    opis_cyrlat = lat_to_cyr(opis) + ' ' + cyr_to_lat(opis)
    document = {
        'pk': publikacija.id,
        'potkorpus': publikacija.potkorpus.naziv if publikacija.potkorpus else '',
        'skracenica': publikacija.skracenica,
        'opis': opis,
        'content': opis_cyrlat,
        'timestamp': datetime.now().isoformat()[:-3] + 'Z',
    }
    try:
        if not client:
            client = get_es_client()
        client.index(index=NASLOV_INDEX, id=publikacija.id, document=document)
    except Exception as ex:
        log.fatal(ex)
        return False
    return True


def index_imenica(imenica, client=None):
    oo = imenica.nomjed
    if not oo:
        oo = imenica.nommno
    imenica_dict = {
        'pk': '0_' + str(imenica.pk),
        'rec': oo,
        'vrsta': 0,
        'oblici': imenica.oblici(),
        'osnovni_oblik': imenica.nomjed,
    }
    return save_dict(imenica_dict, client)


def index_glagol(glagol, client=None):
    glagol_dict = {
        'pk': '1_' + str(glagol.pk),
        'rec': glagol.infinitiv,
        'vrsta': 1,
        'oblici': glagol.oblici(),
        'osnovni_oblik': glagol.infinitiv,
    }
    return save_dict(glagol_dict, client)


def index_pridev(pridev, client=None):
    oo = pridev.lema
    if not oo:
        oo = pridev.mpnomjed or pridev.monomjed
    pridev_dict = {
        'pk': '2_' + str(pridev.pk),
        'rec': oo,
        'vrsta': 2,
        'oblici': pridev.oblici(),
        'osnovni_oblik': pridev.lema,
    }
    return save_dict(pridev_dict, client)


def index_predlog(predlog, client=None):
    predlog_dict = {
        'pk': '4_' + str(predlog.pk),
        'rec': predlog.tekst,
        'vrsta': 4,
        'oblici': predlog.oblici(),
        'osnovni_oblik': predlog.tekst,
    }
    return save_dict(predlog_dict, client)


def index_recca(recca, client=None):
    recca_dict = {
        'pk': '7_' + str(recca.pk),
        'rec': recca.tekst,
        'vrsta': 7,
        'oblici': recca.oblici(),
        'osnovni_oblik': recca.tekst,
    }
    return save_dict(recca_dict, client)


def index_uzvik(uzvik, client=None):
    uzvik_dict = {
        'pk': '6_' + str(uzvik.pk),
        'rec': uzvik.tekst,
        'vrsta': 6,
        'oblici': uzvik.oblici(),
        'osnovni_oblik': uzvik.tekst,
    }
    return save_dict(uzvik_dict, client)


def index_veznik(veznik, client=None):
    veznik_dict = {
        'pk': '8_' + str(veznik.pk),
        'rec': veznik.tekst,
        'vrsta': 8,
        'oblici': veznik.oblici(),
        'osnovni_oblik': veznik.tekst,
    }
    return save_dict(veznik_dict, client)


def index_zamenica(zamenica, client=None):
    zamenica_dict = {
        'pk': '5_' + str(zamenica.pk),
        'rec': zamenica.nomjed,
        'vrsta': 5,
        'oblici': zamenica.oblici(),
        'osnovni_oblik': zamenica.osnovni_oblik(),
    }
    return save_dict(zamenica_dict, client)


def index_broj(broj, client=None):
    broj_dict = {
        'pk': '9_' + str(broj.pk),
        'rec': broj.nomjed,
        'vrsta': 9,
        'oblici': broj.oblici(),
        'osnovni_oblik': broj.osnovni_oblik(),
    }
    return save_dict(broj_dict, client)


def index_prilog(prilog, client=None):
    prilog_dict = {
        'pk': '3_' + str(prilog.pk),
        'rec': prilog.pozitiv,
        'vrsta': 3,
        'oblici': prilog.oblici(),
        'osnovni_oblik': prilog.osnovni_oblik(),
    }
    return save_dict(prilog_dict, client)


def save_dict(rec_dict, client=None):
    try:
        oblici = rec_dict['oblici']
        oblici = add_latin(oblici)
        if not oblici:
            log.warning(f'Prazna lista oblika za {rec_dict}')
        var_set = set(oblici)
        varijante = list(var_set)
        rec_sa_varijantama = ' '.join(varijante)
        osnovni_oblik = ' '.join(add_latin(clear_text([rec_dict['rec']], True)))
        rec_dict['oblici'] = rec_sa_varijantama
        rec_dict['osnovni_oblik'] = osnovni_oblik
        rec_dict['oblici_reversed'] = rec_sa_varijantama
        rec_dict['osnovni_oblik_reversed'] = osnovni_oblik
        rec_dict['timestamp'] = datetime.now().isoformat()[:-3] + 'Z'
        if not client:
            client = get_es_client()
        client.index(index=REC_INDEX, id=rec_dict['pk'], document=rec_dict)
        return True
    except Exception as ex:
        log.fatal(ex)
        return False


def remove_word(word_type, word_id):
    """
    Uklanja rec iz indeksa.
    """
    try:
        pk = f'{word_type}_{word_id}'
        client = get_es_client()
        client.delete(index=REC_INDEX, id=pk)
    except Exception as ex:
        log.fatal(ex)
