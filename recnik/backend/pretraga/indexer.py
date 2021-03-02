from django.conf import settings
from elasticsearch_dsl import analyzer, Index
from elasticsearch_dsl.connections import connections
from .models import OdrednicaDocument, KorpusDocument
from .serializers import CreateOdrednicaDocumentSerializer
from .config import *

def check_elasticsearch():
    pass


def create_index_if_needed():
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


def recreate_index():
    if connections.get_connection().indices.exists(ODREDNICA_INDEX):
        connections.get_connection().indices.delete(ODREDNICA_INDEX)
    if connections.get_connection().indices.exists(KORPUS_INDEX):
        connections.get_connection().indices.delete(KORPUS_INDEX)
        create_index_if_needed()


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
    result = odrednica.save(id=odrednica.pk, index=ODREDNICA_INDEX)
    return result
