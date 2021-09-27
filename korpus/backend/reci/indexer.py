import logging
from django.conf import settings
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections
from .models import Imenica
import requests
from django.conf import settings
from elasticsearch_dsl import analyzer, Index
from elasticsearch_dsl.connections import connections
from elasticsearch.exceptions import ElasticsearchException, NotFoundError
from .models import OdrednicaDocument, KorpusDocument
from .serializers import CreateOdrednicaDocumentSerializer, CreatePublikacijaDocumentSerializer

log = logging.getLogger(__name__)

KORPUS_INDEX = 'korpus'
ALL_INDEXES = [
    {'index': KORPUS_INDEX, 'document': KorpusDocument},
]
SERBIAN_ANALYZER = analyzer('serbian')

try:
    connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST], timeout=20)
except Exception as ex:
    log.fatal(ex)


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


def save_imenica_model(imenica):
    oblici = []
    imenica_dict = {
        'vrsta': 0,
        'podvrsta': imenica.vrsta,
        'pk': imenica.pk,
        'oblici': oblici,
    }
    return save_dict(imenica_dict)


def save_dict(odr_dict):
    serializer = CreateOdrednicaDocumentSerializer()
    odrednica = serializer.create(odr_dict)
    try:
        result = odrednica.save(id=odrednica.pk, index=KORPUS_INDEX)
        return result
    except Exception as ex:
        log.fatal(ex)
        return None


def delete_imenica(imenica_id):
    odrednica = OdrednicaDocument()
    try:
        # TODO: select properly
        odrednica.delete(id=imenica_id, index=KORPUS_INDEX)
    except NotFoundError:
        return False
    except ElasticsearchException:
        return False
    return True
