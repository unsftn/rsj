from datetime import datetime
import logging
import re
import unicodedata
import requests
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from elasticsearch import Elasticsearch
from elasticsearch_dsl import analyzer, Index, Document, Keyword, SearchAsYouType, Search, Text, Date
from elasticsearch_dsl.connections import connections
from .cyrlat import cyr_to_lat

log = logging.getLogger(__name__)


def init_es_connection():
    try:
        connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST])
    except Exception as exc:
        log.fatal(exc)


class TimestampedDocument(Document):
    timestamp = Date()

    def save(self, **kwargs):
        if not self.timestamp:
            self.timestamp = datetime.now()
        return super().save(**kwargs)


class RecDocument(TimestampedDocument):
    pk = Keyword()
    rec = Keyword()
    vrsta = Keyword()
    oblici = SearchAsYouType()

    def __str__(self):
        return f'{self.pk} | {self.vrsta} | {self.rec} | {self.oblici}'


class PubDocument(TimestampedDocument):
    pk = Keyword()
    skracenica = Keyword()
    opis = Keyword()
    tekst = Text()


SERBIAN_ANALYZER = analyzer('serbian')
PUB_INDEX = 'publikacije'
REC_INDEX = 'reci'
ALL_INDEXES = {
    PUB_INDEX: {'index': PUB_INDEX, 'document': PubDocument},
    REC_INDEX: {'index': REC_INDEX, 'document': RecDocument},
}
REGEX_CONTAINS_PARENTHESES = re.compile('(.+)\\((.*?)\\)(.*?)')


def remove_punctuation(text):
    cleared_text = ''.join(c for c in text if unicodedata.category(c) in ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'NI', 'Zs'])
    return cleared_text


def clear_text(obj):
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
            else:
                new_list.append(item)
        return new_list
    return obj


def add_latin(lst):
    result = []
    result.extend(lst)
    for item in lst:
        result.append(cyr_to_lat(item))
    return result

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
        client = Elasticsearch()
        for es_idx in ALL_INDEXES.values():
            if not client.indices.exists(es_idx['index']):
                idx = Index(es_idx['index'])
                idx.analyzer(SERBIAN_ANALYZER)
                idx.document(es_idx['document'])
                idx.create()
    except Exception as ex:
        log.fatal(ex)


def recreate_index(index=None):
    indexes = [ALL_INDEXES[index]] if index else ALL_INDEXES.values()
    client = Elasticsearch()
    try:
        for es_idx in indexes:
            if client.indices.exists(es_idx['index']):
                client.indices.delete(es_idx['index'])
        create_index_if_needed()
    except Exception as ex:
        log.fatal(ex)


def push_highlighting_limit():
    payload = {
        'index': {
            'highlight.max_analyzed_offset': 100000000
        }
    }
    if check_elasticsearch():
        r = requests.put(f'http://{settings.ELASTICSEARCH_HOST}:9200/publikacije/_settings', json=payload)
        return r.status_code == 200
    else:
        return False


class RecSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    rec = serializers.CharField(max_length=50, required=True)
    vrsta = serializers.IntegerField(required=True)
    oblici = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        model = RecDocument
        fields = ('pk', 'rec', 'vrsta', 'oblici')

    def create(self, validated_data):
        pk = validated_data.pop('pk')
        rec = validated_data.pop('rec')
        oblici = validated_data.pop('oblici', [])
        oblici = clear_text(oblici)
        oblici = add_latin(oblici)
        var_set = set(oblici)
        varijante = list(var_set)
        rec_sa_varijantama = ' '.join(varijante)
        vrsta = validated_data.pop('vrsta')
        return RecDocument(pk=pk, rec=rec, oblici=rec_sa_varijantama, vrsta=vrsta)


class PubSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    skracenica = serializers.CharField(max_length=100, required=True)
    opis = serializers.CharField(max_length=1000, required=True)
    tekst = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = PubDocument
        fields = ('pk', 'tekst')

    def create(self, validated_data):
        pk = validated_data.pop('pk')
        tekst = validated_data.pop('tekst')
        skracenica = validated_data.pop('skracenica')
        opis = validated_data.pop('opis')
        return PubDocument(pk=pk, tekst=tekst, skracenica=skracenica, opis=opis)


JSON = 'application/json'


def bad_request(error):
    return Response(error, status=HTTP_400_BAD_REQUEST, content_type=JSON)


def not_found(error):
    return Response(error, status=HTTP_404_NOT_FOUND, content_type=JSON)


def server_error(error):
    return Response(error, status=HTTP_500_INTERNAL_SERVER_ERROR, content_type=JSON)
