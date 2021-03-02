from django.conf import settings
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections

ODREDNICA_INDEX = 'odrednica'
KORPUS_INDEX = 'korpus'
SERBIAN_ANALYZER = analyzer('serbian')
connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST], timeout=20)
