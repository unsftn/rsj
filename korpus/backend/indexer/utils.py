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
        "potkorpus": {
            "type": "keyword"
        },
        "tekst": {
            "type": "text",
            "term_vector": "with_positions_offsets",
            "store": "true",
        },
        "tekst_reversed": {
            "type": "text",
            "term_vector": "with_positions_offsets",
            "store": "true",
            "analyzer": "reversed"
        },
        "tekst_case_sensitive": {
            "type": "text",
            "term_vector": "with_positions_offsets",
            "store": "true",
            "analyzer": "case_sensitive"
        },
        "timestamp": {
            "type": "date"
        }
    }
}
PUB_SETTINGS = {
    "analysis": {
        "analyzer": {
            "reversed": {
                "tokenizer": "standard",
                "filter": ["reverse"]
            },
            "case_sensitive": {
                "tokenizer": "standard",
                "filter": ["stop"]
            }
        }
    }
}


""" Definicija Elasticsearch indeksa za reci """
REC_MAPPING = {
    "properties": {
        "oblici": {
            "type": "search_as_you_type",
            "doc_values": False,
            # "max_shingle_size": 3,
            "analyzer": "whitespace",
        },
        "oblici_reversed": {
            "type": "search_as_you_type",
            "doc_values": False,
            # "max_shingle_size": 3,
            "analyzer": "reversed"
        },
        "osnovni_oblik": {
            "type": "search_as_you_type",
            "doc_values": False,
            # "max_shingle_size": 3,
            "analyzer": "whitespace",
        },
        "osnovni_oblik_reversed": {
            "type": "search_as_you_type",
            "doc_values": False,
            # "max_shingle_size": 3,
            "analyzer": "reversed"
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
REC_SETTINGS = {
    "analysis": {
        "analyzer": {
            "reversed": {
                "tokenizer": "standard",
                "filter": ["reverse"]
            },
            "whitespace": {
                "tokenizer": "whitespace",
                "filter": ["stop"]
            }
        }
    }
}


""" Definicija Elasticsearch indeksa za naslove """
NASLOV_MAPPING = {
    "properties": {
        "content": {
            "type": "text"
        },
        "opis": {
            "type": "keyword"
        },
        "pk": {
            "type": "keyword"
        },
        "skracenica": {
            "type": "keyword"
        },
        "timestamp": {
            "type": "date"
        },
        "potkorpus": {
            "type": "keyword"
        },
    }
}


PUB_INDEX = 'publikacije'
REVERSE_INDEX = 'reverse'
CASE_SENSITIVE_INDEX = 'casesensitive'
REC_INDEX = 'reci'
NASLOV_INDEX = 'naslovi'
ALL_INDEXES = {
    PUB_INDEX: {'index': PUB_INDEX, 'mapping': PUB_MAPPING, 'settings': PUB_SETTINGS},
    REC_INDEX: {'index': REC_INDEX, 'mapping': REC_MAPPING, 'settings': REC_SETTINGS},
    NASLOV_INDEX: {'index': NASLOV_INDEX, 'mapping': NASLOV_MAPPING, 'settings': None},
}
REGEX_CONTAINS_PARENTHESES = re.compile('(.+)\\((.*?)\\)(.*?)')


def contains_non_cyrillic_chars(text):
    """
    Vraca true ako string sadrzi ne-cirilicke znake.
    """
    return regex.fullmatch('\\p{IsCyrillic}*', text) is None
    

def contains_non_cyrillic_chars_or_dash(text):
    """
    Vraca true ako string sadrzi ne-cirilicke znake.
    """
    return regex.fullmatch('(\\p{IsCyrillic}|-)*', text) is None
    

def remove_punctuation(text):
    """
    Uklanja znake interpunkcije iz stringa i vraca novi string
    """
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    cleared_text = ''.join((c if unicodedata.category(c) in ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'NI', 'Zs'] else ' ') for c in text)
    return cleared_text


def remove_punctuation_remain_dash(text):
    """
    Uklanja znake interpunkcije iz stringa i vraca novi string
    """
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    cleared_text = ''.join((c if unicodedata.category(c) in ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'NI', 'Zs'] else ('-' if c in ['-', '\u2010', '\u2011', '\u2012', '\u2013', '\u2014'] else ' ')) for c in text)
    if cleared_text and cleared_text[-1] == '-':
        cleared_text = cleared_text[:-1]
    return cleared_text


def clear_text(obj, remain_dash=False):
    """
    Cisti tekst za pretragu:
    - ako je ulaz string, vraca ociscen string
    - ako je ulaz lista stringova, vraca listu ociscenih stringova
    """
    if not obj:
        return obj
    clear_func = remove_punctuation_remain_dash if remain_dash else remove_punctuation

    if isinstance(obj, str):
        if not REGEX_CONTAINS_PARENTHESES.match(obj):
            return clear_func(obj)
        else:
            return [clear_func(REGEX_CONTAINS_PARENTHESES.sub('\\1\\3', obj)),
                    clear_func(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2\\3', obj))]
    if isinstance(obj, list):
        new_list = []
        for item in obj:
            if isinstance(item, str):
                if not REGEX_CONTAINS_PARENTHESES.match(item):
                    new_list.append(clear_func(item))
                else:
                    new_list.append(clear_func(REGEX_CONTAINS_PARENTHESES.sub('\\1\\3', item)))
                    new_list.append(clear_func(REGEX_CONTAINS_PARENTHESES.sub('\\1\\2\\3', item)))
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
        log.fatal('Error checking for Elasticsearch')
        log.fatal(ex)
        return False


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
            if es_idx['settings']:
                client.indices.create(index=es_idx['index'], mappings=es_idx['mapping'], settings=es_idx['settings'])
            else:
                client.indices.create(index=es_idx['index'], mappings=es_idx['mapping'])
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
        r = requests.put(f'{settings.ELASTICSEARCH_HOST}/{PUB_INDEX}/_settings', json=payload)
        if r.status_code != 200:
            return False
        r = requests.put(f'{settings.ELASTICSEARCH_HOST}/{REVERSE_INDEX}/_settings', json=payload)
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
