from django.conf import settings
from elasticsearch.exceptions import NotFoundError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
import requests
from odrednice.models import Odrednica, VRSTA_ODREDNICE
from odrednice.text import remove_punctuation
from render.utils import get_rbr, get_rec, shorten_text
from .serializers import *
from .config import *
from .cyrlat import sort_key

JSON = 'application/json'
AZBUKA = 'абвгдђежзијклљмнњопрстћуфхцчџш'


def sort_key_composite(word):
    rbr_homo = word['rbr_homo'] if word['rbr_homo'] else 0
    result = sort_key(word['ociscena_rec'])
    result.append(rbr_homo)
    return result


@api_view(['GET'])
def odrednica(request):
    if not request.GET.get('q'):
        return bad_request('no search term')
    term = request.GET.get('q')

    term = remove_punctuation(term)
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
    resp = get_es_client().search(index=ODREDNICA_INDEX, body=query)
    for hit in resp['hits']['hits']:
        hits.append({
            'pk': hit['_source']['pk'],
            'rec': hit['_source']['rec'],
            'vrsta': hit['_source']['vrsta'],
            'vrsta_text': VRSTA_ODREDNICE[hit['_source']['vrsta']][1],
            'rbr_homo': hit['_source']['rbr_homo'],
            'ociscena_rec': hit['_source']['ociscena_rec'],
        })
    result = sorted(hits, key=lambda w: sort_key_composite(w))
    return Response(result, status=HTTP_200_OK)


@api_view(['GET'])
def check_duplicate(request):
    term = request.GET.get('q')
    sid = request.GET.get('id')
    shomo = request.GET.get('homo')
    svrsta = request.GET.get('vrsta')
    termid = int(sid) if sid else None
    rbr_homo = int(shomo) if shomo else None
    vrsta = int(svrsta) if svrsta else None
    hits = []

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
    resp = get_es_client().search(index=ODREDNICA_INDEX, body=query)
    for hit in resp['hits']['hits']:
        try:
            found_homo = hit['_source']['rbr_homo']
        except KeyError:
            found_homo = None

        # ako je nova rec
        if termid is None:
            append_to_hits(hits, termid, vrsta, term, hit, found_homo, rbr_homo)
        # ako je postojeca rec a nije ona sama
        elif hit['_source']['rec'] == term and hit['_source']['pk'] != termid:
            append_to_hits(hits, termid, vrsta, term, hit, found_homo, rbr_homo)

    result = sorted(hits, key=lambda w: sort_key_composite(w))
    return Response(result)


@api_view(['GET'])
def search_opis_in_korpus(request):
    """
    Pretrazuje opise izvora u korpusu za dati tekst
    """
    if not request.GET.get('q'):
        return bad_request('no search term')
    term = request.GET.get('q')
    if not term.endswith('*'):
        term += '*'
    query = {
        'query': {'query_string': {'query': term}},
        'size': 100,
        'from': 0,
        '_source': {'includes': ['pk', 'skracenica', 'opis']}
    }
    retval = []
    resp = get_korpus_client().search(index=NASLOV_INDEX, body=query)
    for hit in resp['hits']['hits']:
        retval.append({
            'pub_id': hit['_source']['pk'],
            'skracenica': hit['_source']['skracenica'],
            'opis': hit['_source']['opis'],
        })
    return Response(retval, status=HTTP_200_OK, content_type=JSON)


@api_view(['GET'])
def load_opis_from_korpus_wrapped(request, izvor_id):
    retval = load_opis_from_korpus(izvor_id)
    if retval is None:
        return Response(None, status=HTTP_404_NOT_FOUND, content_type=JSON)
    return Response(retval, status=HTTP_200_OK, content_type=JSON)


def load_opis_from_korpus(izvor_id):
    """
    Ucitava opis izvora za dati ID izvora u korpusu
    """
    if not izvor_id:
        return None
    resp = requests.get(f'{settings.KORPUS_URL}/api/publikacije/opis/{izvor_id}/')
    if resp.status_code == 200:
        return resp.json()
    return None


@api_view(['GET'])
def search_odrednica_sa_znacenjima(request):
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    query = {
        'query': {
            'multi_match': {
                'type': 'bool_prefix',
                'query': remove_punctuation(term),
                'fields': ['varijante']
            }
        },
        'from': 0,
        'size': 100,
        '_source': {
            'includes': ['pk', 'rec', 'vrsta', 'rbr_homo']
        }
    }
    try:
        response = Elasticsearch(hosts=settings.ELASTICSEARCH_HOST).search(index=ODREDNICA_INDEX, body=query)
        odrednice = []
        odr_ids = [x['_source']['pk'] for x in response['hits']['hits']]
        odrednice = Odrednica.objects.filter(id__in=odr_ids)
        retval = []
        for odr in odrednice:
            flatten = False
            if odr.znacenje_set.count() == 1:
                if odr.znacenje_set.first().podznacenje_set.count() == 0:
                    flatten = True
            rec = get_rec(odr)
            retval.append({
                'type': 'odrednica',
                'vrsta': 1,
                'tekst': shorten_text(odr.znacenje_set.first().tekst if flatten else ''),
                'ident': odr.znacenje_set.first().id if flatten else odr.id,
                'odr': rec,
                'rbr': '1' if flatten else '',
                'rbr_homo': odr.rbr_homonima,
                'ociscena_rec': odr.sortable_rec,
            })
            if not flatten:
                for z in odr.znacenje_set.all():
                    if z.tekst:
                        retval.append({
                            'type': 'znacenje',
                            'vrsta': 2,
                            'tekst': f'{z.tekst[:40]}',
                            'ident': z.id,
                            'odr': rec,
                            'rbr': get_rbr(z),
                            'rbr_homo': odr.rbr_homonima,
                            'ociscena_rec': odr.sortable_rec,
                        })
                    for pz in z.podznacenje_set.all():
                        if pz.tekst:
                            retval.append({
                                'type': 'podznacenje',
                                'vrsta': 3,
                                'tekst': f'{pz.tekst[:40]}',
                                'ident': pz.id,
                                'odr': rec,
                                'rbr': get_rbr(pz),
                                'rbr_homo': odr.rbr_homonima,
                                'ociscena_rec': odr.sortable_rec,
                            })
        retval = sorted(retval, key=lambda w: sort_key_composite(w))
        return Response(retval, status=HTTP_200_OK)
    except Exception as error:
        return server_error(error)


def append_if_term_and_homo_match(hits, term, hit, found_homo, rbr_homo):
    if hit['_source']['rec'] == term:
        if found_homo:
            if found_homo == rbr_homo:
                hits.append(hit['_source'])
        else:
            hits.append(hit['_source'])


def append_to_hits(hits, termid, vrsta, term, hit, found_homo, rbr_homo):
    if not vrsta:
        append_if_term_and_homo_match(hits, term, hit, found_homo, rbr_homo)
    elif vrsta == hit['_source']['vrsta']:
        append_if_term_and_homo_match(hits, term, hit, found_homo, rbr_homo)


def bad_request(error):
    return Response(error, status=HTTP_400_BAD_REQUEST, content_type=JSON)


def not_found(error):
    return Response(error, status=HTTP_404_NOT_FOUND, content_type=JSON)


def server_error(error):
    return Response(error, status=HTTP_500_INTERNAL_SERVER_ERROR, content_type=JSON)
