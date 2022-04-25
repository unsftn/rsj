from publikacije.models import *
from .utils import *


def index_publikacija(pub_id):
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
        pub.save(id=publikacija.id, index=PUB_INDEX)
        return True
    except Exception as ex:
        log.fatal(ex)
        return False


def index_imenica(imenica):
    imenica_dict = {
        'pk': '0_' + str(imenica.pk),
        'rec': imenica.nomjed,
        'vrsta': 0,
        'oblici': imenica.oblici(),
    }
    return save_dict(imenica_dict)


def index_glagol(glagol):
    glagol_dict = {
        'pk': '1_' + str(glagol.pk),
        'rec': glagol.infinitiv,
        'vrsta': 1,
        'oblici': glagol.oblici(),
    }
    return save_dict(glagol_dict)


def index_pridev(pridev):
    pridev_dict = {
        'pk': '2_' + str(pridev.pk),
        'rec': pridev.lema,
        'vrsta': 2,
        'oblici': pridev.oblici(),
    }
    return save_dict(pridev_dict)


def save_dict(rec_dict):
    serializer = RecSerializer()
    rec = serializer.create(rec_dict)
    try:
        result = rec.save(id=rec.pk, index=REC_INDEX)
        return result
    except Exception as ex:
        log.fatal(ex)
        return None


def delete_imenica(imenica_id):
    # TODO ovo moze da radi za sve vrste reci
    imenica = RecDocument()
    try:
        # TODO: select properly
        imenica.delete(id=imenica_id, index=REC_INDEX)
    except NotFoundError:
        return False
    except ElasticsearchException:
        return False
    return True


