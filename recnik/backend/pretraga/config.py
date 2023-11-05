import logging
from django.conf import settings
from elasticsearch import Elasticsearch

log = logging.getLogger(__name__)

ODREDNICA_INDEX = 'odrednica'
NASLOV_INDEX = 'naslovi'


def get_es_client():
    return Elasticsearch(hosts=settings.ELASTICSEARCH_HOST)


def get_korpus_client():
    return Elasticsearch(hosts=settings.KORPUS_HOST)


ODREDNICA_MAPPING = {
    "properties": {
        "pk": {
            "type": "keyword"
        },
        "rec": {
            "type": "keyword"
        },
        "ociscena_rec": {
            "type": "keyword"
        },
        "varijante": {
            "type": "search_as_you_type",
            "doc_values": False,
            "max_shingle_size": 3
        },
        "vrsta": {
            "type": "keyword"
        },
        "rbr_homo": {
            "type": "keyword"
        },
        "status": {
            "type": "keyword"
        }
    }
}
