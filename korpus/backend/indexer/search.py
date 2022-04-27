from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK
from elasticsearch import Elasticsearch, ElasticsearchException
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from .utils import *
from reci.models import *


@api_view(['GET'])
def search_rec(request):
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    hits = []
    try:
        client = get_es_client()
        s = Search(using=client, index=REC_INDEX)
        s = s.source(includes=['pk', 'rec', 'vrsta', 'podvrsta'])[:25]
        s.query = MultiMatch(type='bool_prefix', query=remove_punctuation(term), fields=['oblici'])
        response = s.execute()
        for hit in response.hits.hits:
            hits.append({
                'vrsta': hit['_source']['vrsta'],
                'vrsta_text': VRSTE_RECI[hit['_source']['vrsta']],
                'rec': hit['_source']['rec'],
                'pk': int(hit['_source']['pk'].split('_')[1])
            })
        result = sorted(hits, key=lambda x: x['rec'])
        return Response(result, status=HTTP_200_OK, content_type=JSON)
    except ElasticsearchException as error:
        return server_error(error.args)
    except Exception as error:
        log.fatal(error)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_pub(request):
    if not request.GET.get('w'):
        return bad_request('no search word')
    if not request.GET.get('t'):
        return bad_request('no word type')
    if request.GET.get('f'):
        fragment_size = int(request.GET.get('f'))
    else:
        fragment_size = 150

    word_id = int(request.GET.get('w'))
    word_type = int(request.GET.get('t'))
    if word_type == 0:
        oblici = Imenica.objects.get(pk=word_id).oblici()
    elif word_type == 1:
        oblici = Glagol.objects.get(pk=word_id).oblici()
    elif word_type == 2:
        oblici = Pridev.objects.get(pk=word_id).oblici()
    else:
        oblici = []
    client = get_es_client()
    s = Search(using=client, index=PUB_INDEX).source(includes=['pk', 'tekst', 'skracenica', 'opis']).query('terms', tekst=oblici)\
        .highlight('tekst', fragment_size=fragment_size, type='plain', boundary_scanner='word',
                   number_of_fragments=200, pre_tags=['<span class="highlight">'], post_tags=['</span>'])
    try:
        retval = []
        response = s.execute()
        for hit in response.hits.hits:
            try:
                hit['highlight']
                highlights = [t for t in hit.highlight.tekst]
            except KeyError:
                highlights = []
            retval.append({
                'pub_id': hit._source.pk,
                'skracenica': hit._source.skracenica,
                'opis': hit._source.opis,
                'highlights': highlights,
            })
        return Response(retval, status=HTTP_200_OK, content_type=JSON)
    except ElasticsearchException as error:
        return server_error(error.args)
