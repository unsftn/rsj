import json
import logging
# from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from .cyrlat import cyr_to_lat, lat_to_cyr, sort_key
from .utils import *
from reci.models import *
from publikacije.models import *
from publikacije.serializers import PublikacijaSerializer2

logger = logging.getLogger(__name__)


MAX_TERM_CHUNK_SIZE = 10


@api_view(['GET'])
def search_rec(request):
    """
    Pretrazuje rec u medju osnovnim oblicima u bazi obradjenih reci
    """
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    query = {
        'query': {
            'multi_match': {
                'type': 'bool_prefix', 
                'query': remove_punctuation_remain_dash(term).strip(), 
                'fields': ['osnovni_oblik']
            }
        }, 
        'from': 0, 
        'size': 10000, 
        '_source': {
            'includes': ['pk', 'rec', 'vrsta', 'podvrsta']
        }
    }
    print(json.dumps(query, indent=2))
    return _search_word(query)


@api_view(['GET'])
def search_rec_sufiks(request):
    """
    Pretrazuje rec u medju osnovnim oblicima u bazi obradjenih reci
    """
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    query = {
        'query': {
            'query_string': {
                'query': f'{remove_punctuation_remain_dash(term).strip()[::-1]}*', 
                'fields': ['osnovni_oblik_reversed']
            }
        }, 
        'from': 0, 
        'size': 10000, 
        '_source': {
            'includes': ['pk', 'rec', 'vrsta', 'podvrsta']
        }
    }
    return _search_word(query)


def _search_word(query):
    try:
        hits = []
        resp = get_es_client().search(index=REC_INDEX, body=query)
        for hit in resp['hits']['hits']:
            hits.append({
                'vrsta': hit['_source']['vrsta'],
                'vrsta_text': VRSTE_RECI[hit['_source']['vrsta']],
                'rec': hit['_source']['rec'],
                'pk': int(hit['_source']['pk'].split('_')[1])
            })
        result = sorted(hits, key=lambda x: sort_key(x['rec']))
        return Response(result, status=HTTP_200_OK, content_type=JSON)
    except Exception as error:
        log.fatal(error)
        return server_error(error.args)



@api_view(['GET'])
def search_pub(request):
    """
    Pretrazuje publikacije za svim oblicima datog osnovnog oblika.
    """
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
    add_latin_versions(oblici)
    oblici = lowercase(oblici)
    oblici = list(set(oblici))
    return wrap_search(oblici, fragment_size, boundary_scanner)


@api_view(['GET'])
def search_oblik_in_pub(request):
    """
    Pretrazuje tekstove publikacija za datu rec, bez drugih oblika.
    """
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
    case_sensitive = request.GET.get('cs', '') == 'true'

    term = request.GET.get('q').strip()
    suffix = term.startswith('~')
    if suffix:
        term = term[1:]
    prefix = term.endswith('~')
    if prefix:
        term = term[:-1]
    term_cyr = lat_to_cyr(term) #.lower()
    term_lat = cyr_to_lat(term) #.lower()
    query_terms = []
    if term_cyr:
        query_terms.append(term_cyr)
    if term_lat:
        query_terms.append(term_lat)
    return wrap_search(query_terms, fragment_size, boundary_scanner, prefix, suffix, case_sensitive)


@api_view(['GET'])
def search_naslov(request):
    """
    Pretrazuje opise publikacija za dati tekst
    """
    if not request.GET.get('q'):
        return bad_request('no search term')
    term = request.GET.get('q')
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    if not term.endswith('*'):
        term += '*'
    query = {
        'query': {'query_string': {'query': term}},
        'size': 100,
        'from': 0,
        '_source': {'includes': ['pk', 'skracenica', 'opis', 'potkorpus']}
    }
    pubids = []
    resp = get_es_client().search(index=NASLOV_INDEX, body=query)
    for hit in resp['hits']['hits']:
        pubids.append(hit['_source']['pk'])
        # retval.append({
        #     'pub_id': hit['_source']['pk'],
        #     'skracenica': hit['_source']['skracenica'],
        #     'opis': hit['_source']['opis'],
        # })
    queryset = Publikacija.objects.filter(pk__in=pubids).order_by('pk')
    count = len(queryset)
    if offset and limit:
        try:
            o = int(offset)
            l = int(limit)
            queryset = queryset[o:o+l]
        except ValueError:
            pass
    data = PublikacijaSerializer2(queryset, many=True).data
    retval = {'count': count, 'results': data }
    return Response(retval, status=HTTP_200_OK, content_type=JSON)


@api_view(['GET'])
def check_dupes(request):
    if not request.GET.get('w'):
        return bad_request('no search term')
    text = request.GET.get('w')
    word_id = request.GET.get('id')
    if word_id:
        word_id = int(word_id)
    possible_dupes = find_osnovni_oblik(text)
    possible_dupes = [dict(item, vrsta_text=VRSTE_RECI[item['vrsta']]) for item in possible_dupes if item['id'] != word_id]
    return Response(possible_dupes, status=HTTP_200_OK)


def wrap_search(words, fragment_size, boundary_scanner, prefix: bool = False, suffix: bool = False, case_sensitive: bool = False):
    try:
        return Response(
            _search(words, fragment_size, boundary_scanner, prefix, suffix, case_sensitive), 
            status=HTTP_200_OK, 
            content_type=JSON)
    except Exception as error:
        log.fatal(error)
        return server_error(error.args)


def _search(words, fragment_size, boundary_scanner, prefix: bool = False, suffix: bool = False, case_sensitive: bool = False):
    """
    Highlighting ne radi za preveliki broj termova u pretrazi. Zato radimo
    pretragu rec po rec.
    """
    retval = []
    for word in words:
        res = _search_single_word(word, fragment_size, boundary_scanner, prefix, suffix, case_sensitive)
        retval.extend(res)
    retval = sorted(retval, key=lambda x: x['pub_id'])
    retval = [dict(item, order_nr=index+1) for index, item in enumerate(retval)]
    return retval


def _search_single_word(word: str, fragment_size: int, scanner: str, prefix: bool = False, suffix: bool = False, case_sensitive: bool = False):
    """
    Pretrazuje tekstove publikacija za reci date u listi words, sa datom 
    velicinom fragmenta i vrstom granice ('word', 'sentence'). 
    """
    if prefix:
        term = f'{word}*'
        field = 'tekst_case_sensitive' if case_sensitive else 'tekst'
    elif suffix:
        term = f'*{word}'
        field = 'tekst_reversed'
    else:
        term = word
        field = 'tekst_case_sensitive' if case_sensitive else ('tekst_whitespace' if '-' in word else 'tekst')
    query = {
        'query': {
            'query_string': { 'query': term, 'fields': [field] }
        }, 
        'size': 100000,
        '_source': {
            'includes': ['pk', 'skracenica', 'opis', 'potkorpus']
        }, 
        'highlight': {
            'type': 'fvh',
            'fragment_size': fragment_size, 
            'boundary_scanner': scanner, 
            'pre_tags': ['***'], 
            'post_tags': ['***'],
            'fields': {
                field: {}
            }
        }
    }
    retval = []
    resp = get_es_client().search(index=PUB_INDEX, body=query)
    for hit in resp['hits']['hits']:
        try:
            hit['highlight']
            highlights = [t for t in hit['highlight'][field]]
        except KeyError:
            highlights = []
        for high in highlights:                
            retval.append({
                'pub_id': hit['_source']['pk'],
                'potkorpus': hit['_source'].get('potkorpus', ''),
                'skracenica': hit['_source']['skracenica'],
                'opis': hit['_source']['opis'],
                'highlights': high,
            })
    return retval


def find_osnovni_oblik(rec) -> list[dict]:
    """
    Vraca listu recnika koji identifikuju osnovni oblik za datu leksemu. Pozeljno lista
    ima jedan element (tada je nedvosmisleno kojoj reci pripada data leksema).
    """
    retval = []
    resp = get_es_client().search(index=REC_INDEX, query={'terms': {'oblici': [rec]}})
    for hit in resp['hits']['hits']:
        osnovni_oblik = hit['_source']['rec']
        pk = hit['_source']['pk']
        vrsta, id = hit['_source']['pk'].split('_')
        vrsta, id = int(vrsta), int(id)
        retval.append({'rec': osnovni_oblik, 'pk': pk, 'vrsta': vrsta, 'id': id})
    return retval


def chunkify(alist, chunk_size):
    """
    Podeli listu na podliste sa najvise chunk_size elemenata.
    Vraca listu podlista.
    """
    return [alist[i:i + chunk_size] for i in range(0, len(alist), chunk_size)]


def add_latin_versions(words):
    """
    Prosiruje listu leksema latinicnim verzijama
    """
    cyr_list = words[:]
    for leksema in cyr_list:
        lat_verzija = cyr_to_lat(leksema)
        words.append(lat_verzija)
    return words


def lowercase(list_of_words: list) -> list:
    """
    Sve reci u listi stringova pretvara u lowercase. Vraca novu listu.
    """
    retval = []
    for word in list_of_words:
        if word:
            retval.append(word.lower())
    return retval
