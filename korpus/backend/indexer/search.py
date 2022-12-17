from django.conf import settings
import logging
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from .cyrlat import cyr_to_lat, lat_to_cyr
from .utils import *
from reci.models import *

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
    hits = []
    try:
        query = {
            'query': {
                'multi_match': {
                    'type': 'bool_prefix', 
                    'query': remove_punctuation(term), 
                    'fields': ['osnovni_oblik']
                }
            }, 
            'from': 0, 
            'size': 10000, 
            '_source': {
                'includes': ['pk', 'rec', 'vrsta', 'podvrsta']
            }
        }
        resp = get_es_client().search(index=REC_INDEX, body=query)
        for hit in resp['hits']['hits']:
            hits.append({
                'vrsta': hit['_source']['vrsta'],
                'vrsta_text': VRSTE_RECI[hit['_source']['vrsta']],
                'rec': hit['_source']['rec'],
                'pk': int(hit['_source']['pk'].split('_')[1])
            })
        result = sorted(hits, key=lambda x: x['rec'])
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

    term = request.GET.get('q')
    term_cyr = lat_to_cyr(term)
    term_lat = cyr_to_lat(term)
    return wrap_search([term_cyr, term_lat], fragment_size, boundary_scanner)


def wrap_search(words, fragment_size, boundary_scanner):
    try:
        return Response(
            _search(words, fragment_size, boundary_scanner), 
            status=HTTP_200_OK, 
            content_type=JSON)
    except Exception as error:
        log.fatal(error)
        return server_error(error.args)


def _search(words, fragment_size, boundary_scanner):
    """
    Highlighting ne radi za preveliki broj termova u pretrazi. Ukoliko je
    trazeni broj termova veci od MAX_TERM_CHUNK_SIZE, pretragu cemo izvrsiti
    vise puta i ujediniti rezultate. Ujedinjavanje se svodi na dodavanje
    highlight fragmenata na postojeci pogodak.
    """
    chunks = chunkify(words, MAX_TERM_CHUNK_SIZE)
    retval = []
    for chunk in chunks:
        retval.extend(_search_chunk(chunk, fragment_size, boundary_scanner))
    return sorted(retval, key=lambda x: x['pub_id'])


def _search_chunk(words, fragment_size, scanner):
    """
    Pretrazuje tekstove publikacija za reci date u listi words, sa datom 
    velicinom fragmenta i vrstom granice ('word', 'sentence'). 
    """
    query = {
        'query': {
            'terms': {
                'tekst': words
            }
        }, 
        '_source': {
            'includes': ['pk', 'skracenica', 'opis']
        }, 
        'highlight': {
            'fields': {
                'tekst': {
                    'fragment_size': fragment_size, 
                    'type': 'fvh', 
                    'boundary_scanner': scanner, 
                    'number_of_fragments': 1000, 
                    'pre_tags': ['<span class="fword">'], 
                    'post_tags': ['</span>']
                }
            }
        }
    }
    retval = []
    resp = get_es_client().search(index=PUB_INDEX, body=query)
    for hit in resp['hits']['hits']:
        try:
            hit['highlight']
            highlights = [t for t in hit['highlight']['tekst']]
        except KeyError:
            highlights = []
        for high in highlights:                
            retval.append({
                'pub_id': hit['_source']['pk'],
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
