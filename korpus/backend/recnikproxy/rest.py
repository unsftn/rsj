import logging
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from indexer.utils import get_rsj_client
from indexer.cyrlat import sort_key
from publikacije.models import *

log = logging.getLogger(__name__)

VRSTE_RECI = {
    0: 'именица',
    1: 'глагол',
    2: 'придев',
    3: 'прилог',
    4: 'предлог',
    5: 'заменица',
    6: 'узвик',
    7: 'речца',
    8: 'везник',
    9: 'број',
    10: 'остало',
}


def sort_key_composite(word):
    rbr_homo = word['rbr_homo'] if word['rbr_homo'] else 0
    result = sort_key(word['ociscena_rec'])
    result.append(rbr_homo)
    return result


@api_view(['GET'])
def search(request):
    if not request.GET.get('q'):
        return Response('bad request: no query', status=HTTP_400_BAD_REQUEST)
    term = request.GET.get('q')
    # term = remove_punctuation(term)
    if not term.endswith('*'):
        term += '*'
    query = {
        'query': {
            'query_string': {
                'query': term, 
                'fields': ['varijante']
            }
        }, 
        'size': 100,
        'from': 0,
    }
    hits = []
    resp = get_rsj_client().search(index='odrednica', body=query)
    for hit in resp['hits']['hits']:
        hits.append({
            'pk': hit['_source']['pk'],
            'rec': hit['_source']['rec'],
            'vrsta': hit['_source']['vrsta'],
            'vrsta_text': VRSTE_RECI[hit['_source']['vrsta']],
            'rbr_homo': hit['_source']['rbr_homo'],
            'ociscena_rec': hit['_source']['ociscena_rec'],
        })
    result = sorted(hits, key=lambda w: sort_key_composite(w))
    return Response(result, status=HTTP_200_OK)


@api_view(['GET'])
def search2(request):
    if not request.GET.get('q'):
        return Response('bad request: no query', status=HTTP_400_BAD_REQUEST)
    term = request.GET.get('q')
    try:
        url = f'{settings.SEARCH_ENGINE_URL}/odrednica/prefix/{term}'
        resp = requests.get(url, params={'limit': 100})
        resp.raise_for_status()
        data = resp.json()
        hits = []
        for entry in data.get('results', []):
            vrsta = entry['vrsta']
            hits.append({
                'pk': entry['original_id'],
                'rec': entry['rec'],
                'vrsta': vrsta,
                'vrsta_text': VRSTE_RECI.get(vrsta, 'остало'),
                'rbr_homo': entry.get('rbr_homonima'),
                'ociscena_rec': entry['ociscena_rec'],
            })
        result = sorted(hits, key=lambda w: sort_key_composite(w))
        return Response(result, status=HTTP_200_OK)
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return Response(str(error), status=HTTP_500_INTERNAL_SERVER_ERROR)


def fill_primer(primer):
    try:
        pub = Publikacija.objects.get(id=primer['izvor_id'])
        primer['opis'] = pub.opis()
        primer['potkorpus'] = pub.potkorpus_naziv()
        primer['skracenica'] = pub.skracenica
    except Publikacija.DoesNotExist:
        pass


@api_view(['GET'])
def read(request, odrednica_id):
    headers = {
        'Korpus-User': request.user.email,
        'API-Token': settings.KORPUS_API_TOKEN
    }
    host = 'http://localhost:8001' if settings.DEBUG else 'https://recnik.rsj.rs'
    response = requests.get(f'{host}/api/odrednice/external/odrednica/{odrednica_id}/', headers=headers)
    if response.status_code == 200:
        result = response.json()
        for z in result['znacenja']:
            for pr in z['primeri']:
                fill_primer(pr)
            for pz in z['podznacenja']:
                for pr in pz['primeri']:
                    fill_primer(pr)
        return Response(result, status=HTTP_200_OK)
    else:
        return Response(status=response.status_code)


@api_view(['PUT'])
def save(request):
    if not request.data.get('id'):
        return Response('Недостаје идентификатор одреднице', status=HTTP_400_BAD_REQUEST)
    headers = {
        'Korpus-User': request.user.email,
        'API-Token': settings.KORPUS_API_TOKEN
    }
    host = 'http://localhost:8001' if settings.DEBUG else 'https://recnik.rsj.rs'
    response = requests.put(f'{host}/api/odrednice/external/odrednica/{request.data["id"]}/', json=request.data, headers=headers)
    if response.status_code == 204:
        return Response(status=HTTP_204_NO_CONTENT)
    else:
        return Response(response.json(), status=response.status_code)
