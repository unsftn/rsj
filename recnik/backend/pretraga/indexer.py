import requests
from django.conf import settings
from elasticsearch_dsl import analyzer, Index
from elasticsearch_dsl.connections import connections
from .models import OdrednicaDocument, KorpusDocument
from .serializers import CreateOdrednicaDocumentSerializer
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
        if not connections.get_connection().indices.exists(ODREDNICA_INDEX):
            odrednica_index = Index(ODREDNICA_INDEX)
            odrednica_index.analyzer(SERBIAN_ANALYZER)
            odrednica_index.document(OdrednicaDocument)
            odrednica_index.create()
        if not connections.get_connection().indices.exists(KORPUS_INDEX):
            korpus_index = Index(KORPUS_INDEX)
            korpus_index.analyzer(SERBIAN_ANALYZER)
            korpus_index.document(KorpusDocument)
            korpus_index.create()
    except Exception as ex:
        log.fatal(ex)


def recreate_index():
    try:
        if connections.get_connection().indices.exists(ODREDNICA_INDEX):
            connections.get_connection().indices.delete(ODREDNICA_INDEX)
        if connections.get_connection().indices.exists(KORPUS_INDEX):
            connections.get_connection().indices.delete(KORPUS_INDEX)
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
