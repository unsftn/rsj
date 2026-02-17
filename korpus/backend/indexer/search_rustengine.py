import logging
import time
import requests as http_requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .cyrlat import cyr_to_lat, lat_to_cyr, sort_key
from .utils import remove_punctuation_remain_dash, bad_request, server_error, JSON
from reci.models import VRSTE_RECI, Imenica, Glagol, Pridev, Prilog, Predlog, Zamenica, Uzvik, Recca, Veznik, Broj
from publikacije.models import Publikacija
from publikacije.serializers import PublikacijaSerializer2

log = logging.getLogger(__name__)

WORD_TYPE_TO_INT = {
    'imenica': 0, 'glagol': 1, 'pridev': 2, 'prilog': 3,
    'predlog': 4, 'zamenica': 5, 'uzvik': 6, 'recca': 7,
    'veznik': 8, 'broj': 9,
}


def _word_type_to_int(word_type_str):
    return WORD_TYPE_TO_INT.get(word_type_str, 10)


def _es_fragment_size_to_rust(es_size):
    return max(es_size // 7, 10)


@api_view(['GET'])
def search_rec(request):
    """
    Pretrazuje rec medju osnovnim oblicima u bazi obradjenih reci
    """
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    prefix = remove_punctuation_remain_dash(term).strip()
    try:
        url = f'{settings.SEARCH_ENGINE_URL}/morphology/prefix/{prefix}'
        resp = http_requests.get(url, params={'limit': 10000})
        resp.raise_for_status()
        data = resp.json()
        hits = []
        for entry in data.get('results', []):
            vrsta = _word_type_to_int(entry['word_type'])
            original_id = entry.get('original_id')
            if original_id is None:
                continue
            hits.append({
                'vrsta': vrsta,
                'vrsta_text': VRSTE_RECI.get(vrsta, 'остало'),
                'rec': entry['base_form'],
                'pk': original_id,
            })
        result = sorted(hits, key=lambda x: sort_key(x['rec']))
        return Response(result, status=HTTP_200_OK, content_type=JSON)
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


@api_view(['GET'])
def search_rec_sufiks(request):
    """
    Pretrazuje rec u medju osnovnim oblicima u bazi obradjenih reci
    """
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    suffix = remove_punctuation_remain_dash(term).strip()
    try:
        url = f'{settings.SEARCH_ENGINE_URL}/morphology/suffix/{suffix}'
        resp = http_requests.get(url, params={'limit': 10000})
        resp.raise_for_status()
        data = resp.json()
        hits = []
        for entry in data.get('results', []):
            vrsta = _word_type_to_int(entry['word_type'])
            original_id = entry.get('original_id')
            if original_id is None:
                continue
            hits.append({
                'vrsta': vrsta,
                'vrsta_text': VRSTE_RECI.get(vrsta, 'остало'),
                'rec': entry['base_form'],
                'pk': original_id,
            })
        result = sorted(hits, key=lambda x: sort_key(x['rec']))
        return Response(result, status=HTTP_200_OK, content_type=JSON)
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


def _lookup_pub_metadata(doc_ids):
    pubs = Publikacija.objects.filter(pk__in=doc_ids)
    return {pub.pk: pub for pub in pubs}


def _search_in_rust(phrase, fragment_size, mode='word'):
    url = f'{settings.SEARCH_ENGINE_URL}/search'
    payload = {
        'phrase': phrase,
        'fragment_size': _es_fragment_size_to_rust(fragment_size),
        'mode': mode,
    }
    resp = http_requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()


def _search_multi_in_rust(words, fragment_size, mode='word'):
    url = f'{settings.SEARCH_ENGINE_URL}/search/multi'
    payload = {
        'words': words,
        'fragment_size': _es_fragment_size_to_rust(fragment_size),
        'mode': mode,
    }
    resp = http_requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()


def _rust_results_to_pub_hits(data):
    results = data.get('results', [])
    doc_ids = [r['doc_id'] for r in results]
    pub_map = _lookup_pub_metadata(doc_ids)
    retval = []
    for result in results:
        pub = pub_map.get(result['doc_id'])
        if pub is None:
            continue
        for fragment in result.get('fragments', []):
            retval.append({
                'pub_id': result['doc_id'],
                'potkorpus': pub.potkorpus_naziv(),
                'skracenica': pub.skracenica,
                'opis': pub.opis(),
                'highlights': fragment,
            })
    return retval


def add_latin_versions(words):
    cyr_list = words[:]
    for leksema in cyr_list:
        lat_verzija = cyr_to_lat(leksema)
        words.append(lat_verzija)
    return words


def lowercase(list_of_words):
    return [word.lower() for word in list_of_words if word]


@api_view(['GET'])
def search_pub(request):
    """
    Pretrazuje publikacije za svim oblicima datog osnovnog oblika.
    """
    if not request.GET.get('w'):
        return bad_request('no search word')
    if not request.GET.get('t'):
        return bad_request('no word type')
    fragment_size = int(request.GET.get('f', 150))
    boundary_scanner = request.GET.get('s', 'word')

    word_id = int(request.GET.get('w'))
    word_type = int(request.GET.get('t'))
    t0 = time.perf_counter()
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

    try:
        mode = 'sentence' if boundary_scanner == 'sentence' else 'word'
        data = _search_multi_in_rust(oblici, fragment_size, mode)
        retval = _rust_results_to_pub_hits(data)
        retval = sorted(retval, key=lambda x: x['pub_id'])
        retval = [dict(item, order_nr=index+1) for index, item in enumerate(retval)]
        elapsed_ms = (time.perf_counter() - t0) * 1000
        resp = Response(retval, status=HTTP_200_OK, content_type=JSON)
        resp['Server-Timing'] = f'search;dur={elapsed_ms:.2f};desc="search_pub"'
        return resp
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


@api_view(['GET'])
def search_oblik_in_pub(request):
    """
    Pretrazuje tekstove publikacija za datu rec, bez drugih oblika.
    """
    if not request.GET.get('q'):
        return bad_request('no search term')
    fragment_size = int(request.GET.get('f', 150))
    boundary_scanner = request.GET.get('s', 'word')

    term = request.GET.get('q').strip()
    suffix = term.startswith('~')
    if suffix:
        term = term[1:]
    prefix = term.endswith('~')
    if prefix:
        term = term[:-1]

    if suffix:
        phrase = f'~{term}'
    elif prefix:
        phrase = f'{term}~'
    else:
        phrase = term

    term_cyr = lat_to_cyr(term)
    term_lat = cyr_to_lat(term)
    search_terms = set()
    if term_cyr:
        search_terms.add(term_cyr)
    if term_lat:
        search_terms.add(term_lat)
    if not search_terms:
        search_terms.add(term)

    try:
        mode = 'sentence' if boundary_scanner == 'sentence' else 'word'
        all_results = []
        for search_term in search_terms:
            if suffix:
                search_phrase = f'~{search_term}'
            elif prefix:
                search_phrase = f'{search_term}~'
            else:
                search_phrase = search_term
            data = _search_in_rust(search_phrase, fragment_size, mode)
            all_results.extend(data.get('results', []))

        doc_ids = [r['doc_id'] for r in all_results]
        pub_map = _lookup_pub_metadata(doc_ids)
        retval = []
        for result in all_results:
            pub = pub_map.get(result['doc_id'])
            if pub is None:
                continue
            for fragment in result.get('fragments', []):
                retval.append({
                    'pub_id': result['doc_id'],
                    'potkorpus': pub.potkorpus_naziv(),
                    'skracenica': pub.skracenica,
                    'opis': pub.opis(),
                    'highlights': fragment,
                })
        retval = sorted(retval, key=lambda x: x['pub_id'])
        retval = [dict(item, order_nr=index+1) for index, item in enumerate(retval)]
        return Response(retval, status=HTTP_200_OK, content_type=JSON)
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


@api_view(['GET'])
def check_dupes(request):
    if not request.GET.get('w'):
        return bad_request('no search term')
    text = request.GET.get('w')
    word_id = request.GET.get('id')
    if word_id:
        word_id = int(word_id)
    possible_dupes = find_osnovni_oblik(text)
    possible_dupes = [dict(item, vrsta_text=VRSTE_RECI.get(item['vrsta'], 'остало')) for item in possible_dupes if item['id'] != word_id]
    return Response(possible_dupes, status=HTTP_200_OK)


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
    try:
        url = f'{settings.SEARCH_ENGINE_URL}/naslov/prefix/{term}'
        resp = http_requests.get(url, params={'limit': 100})
        resp.raise_for_status()
        data = resp.json()
        pubids = []
        for entry in data.get('results', []):
            original_id = entry.get('original_id')
            if original_id is not None and original_id not in pubids:
                pubids.append(original_id)
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
        retval = {'count': count, 'results': data}
        return Response(retval, status=HTTP_200_OK, content_type=JSON)
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


def find_osnovni_oblik(rec):
    """
    Vraca listu recnika koji identifikuju osnovni oblik za datu leksemu.
    """
    url = f'{settings.SEARCH_ENGINE_URL}/morphology/form/{rec}'
    resp = http_requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    retval = []
    for entry in data.get('results', []):
        original_id = entry.get('original_id')
        if original_id is None:
            continue
        vrsta = _word_type_to_int(entry['word_type'])
        retval.append({
            'rec': entry['base_form'],
            'pk': f'{vrsta}_{original_id}',
            'vrsta': vrsta,
            'id': original_id,
        })
    return retval
