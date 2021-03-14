import logging
from django.conf import settings
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections
from .models import OdrednicaDocument, KorpusDocument, PublikacijaDocument

log = logging.getLogger(__name__)

ODREDNICA_INDEX = 'odrednica'
KORPUS_INDEX = 'korpus'
PUBLIKACIJE_INDEX = 'publikacije'
ALL_INDEXES = [
    {'index': ODREDNICA_INDEX, 'document': OdrednicaDocument},
    {'index': KORPUS_INDEX, 'document': KorpusDocument},
    {'index': PUBLIKACIJE_INDEX, 'document': PublikacijaDocument},
]
SERBIAN_ANALYZER = analyzer('serbian')

try:
    connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST], timeout=20)
except Exception as ex:
    log.fatal(ex)