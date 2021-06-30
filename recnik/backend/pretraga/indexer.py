import requests
from django.conf import settings
from elasticsearch_dsl import analyzer, Index
from elasticsearch_dsl.connections import connections
from elasticsearch.exceptions import ElasticsearchException, NotFoundError
from .models import OdrednicaDocument, KorpusDocument
from .serializers import CreateOdrednicaDocumentSerializer, CreatePublikacijaDocumentSerializer
from .config import *


def check_elasticsearch():
    try:
        r = requests.get(f'http://{settings.ELASTICSEARCH_HOST}:9200/')
        if r.status_code != 200:
            return False
        json = r.json()
        if not json['version']['number']:
            return False
        if int(json['version']['number'].split('.')[0]) < 7:
            return False
        return True
    except requests.exceptions.ConnectionError:
        return False


def create_index_if_needed():
    try:
        for es_idx in ALL_INDEXES:
            if not connections.get_connection().indices.exists(es_idx['index']):
                idx = Index(es_idx['index'])
                idx.analyzer(SERBIAN_ANALYZER)
                idx.document(es_idx['document'])
                idx.create()
    except Exception as ex:
        log.fatal(ex)


def recreate_index():
    try:
        for es_idx in ALL_INDEXES:
            if connections.get_connection().indices.exists(es_idx['index']):
                connections.get_connection().indices.delete(es_idx['index'])
        create_index_if_needed()
    except Exception as ex:
        log.fatal(ex)


def save_odrednica_model(odrednica):
    varijante = []
    if odrednica.ijekavski:
        varijante.append(odrednica.ijekavski)
    for var in odrednica.varijantaodrednice_set.all():
        if var.tekst:
            varijante.append(var.tekst)
        if var.ijekavski:
            varijante.append(var.ijekavski)
    odr_dict = {
        'vrsta': odrednica.vrsta,
        'pk': odrednica.pk,
        'rec': odrednica.rec,
        'varijante': varijante
    }
    return save_odrednica_dict(odr_dict)


def save_odrednica_dict(odr_dict):
    serializer = CreateOdrednicaDocumentSerializer()
    odrednica = serializer.create(odr_dict)
    try:
        result = odrednica.save(id=odrednica.pk, index=ODREDNICA_INDEX)
        return result
    except Exception as ex:
        log.fatal(ex)
        return None


def delete_odrednica(odrednica_id):
    odrednica = OdrednicaDocument()
    try:
        odrednica.delete(id=odrednica_id, index=ODREDNICA_INDEX)
    except NotFoundError:
        return False
    except ElasticsearchException:
        return False
    return True


def save_publikacija_model(publikacija):
    autori = ' '
    for autor in publikacija.autor_set.all():
        autori += autor.ime + ' ' + autor.prezime
    pub_dict = {
        'pk': publikacija.pk,
        'skracenica': publikacija.skracenica,
        'naslov': publikacija.naslov,
        'tekst': ' '.join([publikacija.skracenica, publikacija.naslov, autori])
    }
    return save_publikacija_dict(pub_dict)


def save_publikacija_dict(pub_dict):
    serializer = CreatePublikacijaDocumentSerializer()
    publikacija = serializer.create(pub_dict)
    try:
        result = publikacija.save(id=publikacija.pk, index=PUBLIKACIJE_INDEX)
        return result
    except Exception as ex:
        log.fatal(ex)
        return None
