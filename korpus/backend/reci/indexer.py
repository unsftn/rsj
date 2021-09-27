import logging
import re
import unicodedata

from elasticsearch_dsl.query import MultiMatch
from rest_framework import serializers
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from elasticsearch_dsl import analyzer, Index, Document, Keyword, SearchAsYouType, Search  # , Text
from elasticsearch_dsl.connections import connections
from elasticsearch.exceptions import ElasticsearchException, NotFoundError
from .cyrlat import cyr_to_lat
from .models import VRSTE_RECI

log = logging.getLogger(__name__)


class KorpusDocument(Document):
    pk = Keyword()
    rec = Keyword()
    vrsta = Keyword()
    podvrsta = Keyword()
    oblici = SearchAsYouType()


SERBIAN_ANALYZER = analyzer('serbian')
KORPUS_INDEX = 'korpus'
ALL_INDEXES = [
    {'index': KORPUS_INDEX, 'document': KorpusDocument},
]
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


try:
    connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST], timeout=20)
except Exception as exc:
    log.fatal(exc)


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


@api_view(['GET'])
def search(request):
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    hits = []
    s = Search(index=KORPUS_INDEX)
    s = s.source(includes=['pk', 'rec', 'vrsta', 'podvrsta'])
    s.query = MultiMatch(type='bool_prefix', query=remove_punctuation(term), fields=['oblici'])
    try:
        response = s.execute()
        for hit in response.hits.hits:
            hits.append({
                'vrsta': hit['_source']['vrsta'],
                'vrsta_text': VRSTE_RECI[hit['_source']['vrsta']],
                'podvrsta': hit['_source']['podvrsta'],
                'rec': hit['_source']['rec'],
                'pk': hit['_source']['pk']
            })
        return Response(hits, status=HTTP_200_OK, content_type=JSON)
    except ElasticsearchException as error:
        return server_error(error.args)


class KorpusSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=True)
    rec = serializers.CharField(max_length=50, required=True)
    vrsta = serializers.IntegerField(required=True)
    podvrsta = serializers.IntegerField(required=True)
    oblici = serializers.ListField(child=serializers.CharField(), required=True)

    class Meta:
        model = KorpusDocument
        fields = ('pk', 'rec', 'vrsta', 'podvrsta', 'oblici')

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
        podvrsta = validated_data.pop('podvrsta')
        return KorpusDocument(pk=pk, rec=rec, oblici=rec_sa_varijantama, vrsta=vrsta, podvrsta=podvrsta)


def save_imenica(imenica):
    imenica_dict = {
        'pk': imenica.pk,
        'rec': imenica.nomjed,
        'vrsta': 0,
        'podvrsta': imenica.vrsta,
        'oblici': imenica.oblici(),
    }
    return save_dict(imenica_dict)


def save_dict(rec_dict):
    serializer = KorpusSerializer()
    rec = serializer.create(rec_dict)
    try:
        result = rec.save(id=rec.pk, index=KORPUS_INDEX)
        return result
    except Exception as ex:
        log.fatal(ex)
        return None


def delete_imenica(imenica_id):
    # TODO ovo moze da radi za sve vrste reci
    imenica = KorpusDocument()
    try:
        # TODO: select properly
        imenica.delete(id=imenica_id, index=KORPUS_INDEX)
    except NotFoundError:
        return False
    except ElasticsearchException:
        return False
    return True


JSON = 'application/json'


def bad_request(error):
    return Response(error, status=HTTP_400_BAD_REQUEST, content_type=JSON)


def not_found(error):
    return Response(error, status=HTTP_404_NOT_FOUND, content_type=JSON)


def server_error(error):
    return Response(error, status=HTTP_500_INTERNAL_SERVER_ERROR, content_type=JSON)
