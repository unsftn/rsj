from elasticsearch import Elasticsearch, ElasticsearchException, NotFoundError
from publikacije.models import *
from .utils import *


def index_publikacija(pub_id, client=None):
    try:
        publikacija = Publikacija.objects.get(id=pub_id)
    except Publikacija.DoesNotExist as ex:
        log.fatal(ex)
        return False

    tekst = ''
    for tp in publikacija.tekstpublikacije_set.all().order_by('redni_broj'):
        tekst += tp.tekst + '\n'
    serializer = PubSerializer()
    pub = serializer.create({
        'pk': publikacija.id,
        'skracenica': publikacija.skracenica,
        'opis': publikacija.opis(),
        'tekst': tekst
    })
    try:
        if not client:
            client = get_es_client()
        pub.save(using=client, id=publikacija.id, index=PUB_INDEX)
        return True
    except Exception as ex:
        log.fatal(ex)
        return False


def index_imenica(imenica, client=None):
    imenica_dict = {
        'pk': '0_' + str(imenica.pk),
        'rec': imenica.nomjed,
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
    pridev_dict = {
        'pk': '2_' + str(pridev.pk),
        'rec': pridev.lema,
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


def save_dict(rec_dict, client=None):
    serializer = RecSerializer()
    rec = serializer.create(rec_dict)
    try:
        if not client:
            client = get_es_client()
        result = rec.save(using=client, id=rec.pk, index=REC_INDEX)
        return result
    except Exception as ex:
        log.fatal(ex)
        return None


def delete_imenica(imenica_id):
    # TODO ovo moze da radi za sve vrste reci
    imenica = RecDocument()
    try:
        # TODO: select properly
        client = get_es_client()
        imenica.delete(using=client, id=imenica_id, index=REC_INDEX)
    except NotFoundError:
        return False
    except ElasticsearchException:
        return False
    return True


