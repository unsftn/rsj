import logging
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections
from .models import OdrednicaDocument, KorpusDocument, PublikacijaDocument

log = logging.getLogger(__name__)

ODREDNICA_INDEX = 'odrednica'
NASLOV_INDEX = 'naslovi'
ALL_INDEXES = [
    {'index': ODREDNICA_INDEX, 'document': OdrednicaDocument},
]
SERBIAN_ANALYZER = analyzer('serbian')

try:
    connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST], timeout=20)
except Exception as ex:
    log.fatal(ex)


def get_es_client():
    return Elasticsearch(hosts=settings.ELASTICSEARCH_HOST)


def get_korpus_client():
    return Elasticsearch(hosts=settings.KORPUS_HOST)
