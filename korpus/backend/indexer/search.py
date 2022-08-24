import logging
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from .cyrlat import cyr_to_lat, lat_to_cyr
from .utils import *
from reci.models import *

logger = logging.getLogger(__name__)


@api_view(['GET'])
def search_rec(request):
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    hits = []
    try:
        client = get_es_client()
        s = Search(index=REC_INDEX).using(client)
        s = s.source(includes=['pk', 'rec', 'vrsta', 'podvrsta'])[:25]
        s.query = MultiMatch(type='bool_prefix', query=remove_punctuation(term), fields=['osnovni_oblik'])
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
    except Exception as error:
        print(error)
        log.fatal(error)
        return server_error(error.args)


@api_view(['GET'])
def search_pub(request):
    if not request.GET.get('w'):
        return bad_request('no search word')
    if not request.GET.get('t'):
        return bad_request('no word type')
    if request.GET.get('f'):
        fragment_size = int(request.GET.get('f'))
    else:
        fragment_size = 150
    if request.GET.get('s'):
        boundary_scanner = request.GET.get('s')
    else:
        boundary_scanner = 'word'

    word_id = int(request.GET.get('w'))
    word_type = int(request.GET.get('t'))
    if word_type == 0:
        oblici = Imenica.objects.get(pk=word_id).oblici()
    elif word_type == 1:
        oblici = Glagol.objects.get(pk=word_id).oblici()
    elif word_type == 2:
        oblici = Pridev.objects.get(pk=word_id).oblici()
    elif word_type == 3:
        oblici = Prilog.objects.get(pk=word_id).oblici()
    elif word_type == 4:
        oblici = Predlog.objects.get(pk=word_id).oblici()
    elif word_type == 5:
        oblici = Zamenica.objects.get(pk=word_id).oblici()
    elif word_type == 6:
        oblici = Uzvik.objects.get(pk=word_id).oblici()
    elif word_type == 7:
        oblici = Recca.objects.get(pk=word_id).oblici()
    elif word_type == 8:
        oblici = Veznik.objects.get(pk=word_id).oblici()
    elif word_type == 9:
        oblici = Broj.objects.get(pk=word_id).oblici()
    else:
        oblici = []
    return search(oblici, fragment_size, boundary_scanner)


@api_view(['GET'])
def search_oblik_in_pub(request):
    if not request.GET.get('q'):
        return bad_request('no search term')
    if request.GET.get('f'):
        fragment_size = int(request.GET.get('f'))
    else:
        fragment_size = 150
    if request.GET.get('s'):
        boundary_scanner = request.GET.get('s')
    else:
        boundary_scanner = 'word'

    term = request.GET.get('q')
    term_cyr = lat_to_cyr(term)
    term_lat = cyr_to_lat(term)
    return search([term_cyr, term_lat], fragment_size, boundary_scanner)


def search(words, fragment_size, scanner):
    client = get_es_client()
    s = Search(using=client, index=PUB_INDEX).source(includes=['pk', 'tekst', 'skracenica', 'opis'])\
        .query('terms', tekst=words)\
        .highlight('tekst', fragment_size=fragment_size, type='fvh', boundary_scanner=scanner,
                   number_of_fragments=1000, pre_tags=['<span class="fword">'], post_tags=['</span>'])
    try:
        retval = []
        response = s.execute()
        for hit in response.hits.hits:
            try:
                hit['highlight']
                highlights = [t for t in hit.highlight.tekst]
            except KeyError:
                highlights = []
            for high in highlights:                
                retval.append({
                    'pub_id': hit._source.pk,
                    'skracenica': hit._source.skracenica,
                    'opis': hit._source.opis,
                    'highlights': high,
                })
        return Response(retval, status=HTTP_200_OK, content_type=JSON)
    except Exception as error:
        print(error)
        log.fatal(error)
        return server_error(error.args)
