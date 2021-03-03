import logging
from django.conf import settings
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections

log = logging.getLogger(__name__)

ODREDNICA_INDEX = 'odrednica'
KORPUS_INDEX = 'korpus'
SERBIAN_ANALYZER = analyzer('serbian')
try:
    connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST], timeout=20)
except Exception as ex:
    log.fatal(ex)