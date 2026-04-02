import logging
import requests as http_requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from indexer.cyrlat import sort_key

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

    try:
        url = f'{settings.SEARCH_ENGINE_URL}/odrednica/prefix/{term}'
        resp = http_requests.get(url, params={'limit': 100})
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
