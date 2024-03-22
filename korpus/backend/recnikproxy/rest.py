from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_200_OK
from indexer.utils import get_rsj_client
from indexer.cyrlat import sort_key


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
def read(request):
    pass

@api_view(['PUT'])
def save(request):
    pass
