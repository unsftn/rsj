from datetime import datetime
import logging
import re
import regex
import unicodedata
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from elasticsearch import Elasticsearch
from .cyrlat import cyr_to_lat

log = logging.getLogger(__name__)


def get_es_client():
    return Elasticsearch(hosts=settings.ELASTICSEARCH_HOST)


def get_rsj_client():
    return Elasticsearch(hosts=settings.RSJ_HOST)


""" Definicija Elasticsearch indeksa za publikacije """
PUB_MAPPING = {
    "mappings": {
        "properties": {
            "opis": {
                "type": "keyword"
            },
            "pk": {
                "type": "keyword"
            },
            "skracenica": {
                "type": "keyword"
            },
            "tekst": {
                "type": "text",
                "term_vector": "with_positions_offsets",
                "store": "true",
                # "index_options": "offsets",
                # "analyzer": "simple"
            },
            "timestamp": {
                "type": "date"
            }
        }
    }
}


""" Definicija Elasticsearch indeksa za reci """
REC_MAPPING = {
    "mappings": {
        "properties": {
            "oblici": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3
            },
            "osnovni_oblik": {
                "type": "search_as_you_type",
                "doc_values": False,
                "max_shingle_size": 3
            },
            "pk": {
                "type": "keyword"
            },
            "rec": {
                "type": "keyword"
            },
            "timestamp": {
                "type": "date"
            },
            "vrsta": {
                "type": "keyword"
            }
        }
    }
}


PUB_INDEX = 'publikacije'
REC_INDEX = 'reci'
ALL_INDEXES = {
    PUB_INDEX: {'index': PUB_INDEX, 'document': PUB_MAPPING},
    REC_INDEX: {'index': REC_INDEX, 'document': REC_MAPPING},
}
REGEX_CONTAINS_PARENTHESES = re.compile('(.+)\\((.*?)\\)(.*?)')


def contains_non_cyrillic_chars(text):
    """
    Vraca true ako string sadrzi ne-cirilicke znake.
    """
    return regex.fullmatch('\\p{IsCyrillic}*', text) is None
    

def remove_punctuation(text):
    """
    Uklanja znake interpunkcije iz stringa i vraca novi string
    """
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    cleared_text = ''.join((c if unicodedata.category(c) in ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'NI', 'Zs'] else ' ') for c in text)
    return cleared_text


def clear_text(obj):
    """
    Cisti tekst za pretragu:
    - ako je ulaz string, vraca ociscen string
    - ako je ulaz lista stringova, vraca listu ociscenih stringova
    """
    if not obj:
        return obj
    if isinstance(obj, str):
        if not REGEX_CONTAINS_PARENTHESES.match(obj):
            return remove_punctuation(obj)
        else:
            return [remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\3', obj)),
                    remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2\\3', obj))]
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            if isinstance(item, str):
                if not REGEX_CONTAINS_PARENTHESES.match(item):
                    new_list.append(remove_punctuation(item))
                else:
                    new_list.append(remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\3', item)))
                    new_list.append(remove_punctuation(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2\\3', item)))
            elif item:
                new_list.append(item)
        return new_list
    return obj


def add_latin(lst):
    """
    Listi stringova dodaje nove elemente sa stringovima konvertovanim u latinicu
    """
    if not lst:
        return lst
    result = []
    result.extend(lst)
    for item in lst:
        result.append(cyr_to_lat(item))
    return result


def check_elasticsearch():
    """
    Proverava da li je dostupan Elasticsearch servis
    """
    try:
        host = settings.ELASTICSEARCH_HOST
        r = requests.get(host)
        if r.status_code != 200:
            return False
        json = r.json()
        if not json['version']['number']:
            return False
        if int(json['version']['number'].split('.')[0]) < 8:
            return False
        return True
    except requests.exceptions.ConnectionError as ex:
        log.fatal('Error checking for elasticsearch')
        log.fatal(ex)
        return False


# def create_index_if_needed():
#     """
#     Kreira indekse za reci i publikacije. Vraca status uspeha operacije.
#     """
#     try:
#         r = requests.put(f'{settings.ELASTICSEARCH_HOST}/reci', json=REC_MAPPING)
#         success = r.status_code // 100 == 2
#         r = requests.put(f'{settings.ELASTICSEARCH_HOST}/publikacije', json=PUB_MAPPING)
#         success = (r.status_code // 100 == 2) and success
#         return success
#     except Exception as ex:
#         log.fatal(ex)
#         return False


def recreate_index(index=None):
    """
    Brise indekse pa ih ponovo kreira.
    """
    indexes = [ALL_INDEXES[index]] if index else ALL_INDEXES.values()
    try:
        client = get_es_client()
        for es_idx in indexes:
            if client.indices.exists(index=es_idx['index']):
                client.indices.delete(index=es_idx['index'])
            client.indices.create(index=es_idx['index'], mappings=es_idx['document']['mappings'])
        return True
    except Exception as ex:
        log.exception(f'Error recreating indexes: {indexes}')
        return False


def push_highlighting_limit():
    """
    Povecava limit za highlight servis na 100M
    """
    payload = {
        'index': {
            'max_result_window': 100000,
            'highlight.max_analyzed_offset': 100000000
        }
    }
    if check_elasticsearch():
        r = requests.put(f'{settings.ELASTICSEARCH_HOST}/publikacije/_settings', json=payload)
        return r.status_code == 200
    else:
        return False


JSON = 'application/json'


def bad_request(error):
    return Response(error, status=HTTP_400_BAD_REQUEST, content_type=JSON)


def not_found(error):
    return Response(error, status=HTTP_404_NOT_FOUND, content_type=JSON)


def server_error(error):
    return Response(error, status=HTTP_500_INTERNAL_SERVER_ERROR, content_type=JSON)
