import logging
import requests as http_requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from odrednice.models import Odrednica, VRSTA_ODREDNICE
from odrednice.text import remove_punctuation
from render.utils import get_rbr, get_rec, shorten_text
from .rest import sort_key_composite, append_to_hits, append_if_term_and_homo_match, bad_request, server_error

log = logging.getLogger(__name__)


def _odrednica_prefix_search(term, limit=100):
    url = f'{settings.SEARCH_ENGINE_URL}/odrednica/prefix/{term}'
    resp = http_requests.get(url, params={'limit': limit})
    resp.raise_for_status()
    data = resp.json()
    hits = []
    for entry in data.get('results', []):
        vrsta = entry['vrsta']
        hits.append({
            'pk': entry['original_id'],
            'rec': entry['rec'],
            'vrsta': vrsta,
            'vrsta_text': VRSTA_ODREDNICE[vrsta][1],
            'rbr_homo': entry.get('rbr_homonima'),
            'ociscena_rec': entry['ociscena_rec'],
        })
    return hits


@api_view(['GET'])
def odrednica(request):
    if not request.GET.get('q'):
        return bad_request('no search term')
    term = request.GET.get('q')
    term = remove_punctuation(term)
    try:
        hits = _odrednica_prefix_search(term)
        result = sorted(hits, key=lambda w: sort_key_composite(w))
        return Response(result, status=HTTP_200_OK)
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


@api_view(['GET'])
def check_duplicate(request):
    term = request.GET.get('q')
    sid = request.GET.get('id')
    shomo = request.GET.get('homo')
    svrsta = request.GET.get('vrsta')
    termid = int(sid) if sid else None
    rbr_homo = int(shomo) if shomo else None
    vrsta = int(svrsta) if svrsta else None
    try:
        raw_hits = _odrednica_prefix_search(term)
        hits = []
        for hit in raw_hits:
            found_homo = hit.get('rbr_homo')
            if termid is None:
                append_to_hits(hits, termid, vrsta, term, {'_source': hit}, found_homo, rbr_homo)
            elif hit['rec'] == term and hit['pk'] != termid:
                append_to_hits(hits, termid, vrsta, term, {'_source': hit}, found_homo, rbr_homo)

        result = sorted(hits, key=lambda w: sort_key_composite(w))
        return Response(result)
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


@api_view(['GET'])
def search_odrednica_sa_znacenjima(request):
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    try:
        raw_hits = _odrednica_prefix_search(remove_punctuation(term))
        odr_ids = [hit['pk'] for hit in raw_hits]
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
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


JSON = 'application/json'


@api_view(['GET'])
def search_opis_in_korpus(request):
    """
    Pretrazuje opise izvora u korpusu za dati tekst
    """
    if not request.GET.get('q'):
        return bad_request('no search term')
    term = request.GET.get('q')
    try:
        url = f'{settings.SEARCH_ENGINE_URL}/naslov/prefix/{term}'
        resp = http_requests.get(url, params={'limit': 100})
        resp.raise_for_status()
        data = resp.json()
        retval = []
        for entry in data.get('results', []):
            retval.append({
                'pub_id': entry['original_id'],
                'skracenica': entry['skracenica'],
                'opis': entry['opis'],
            })
        return Response(retval, status=HTTP_200_OK, content_type=JSON)
    except Exception as error:
        log.error(f'Rust engine search error: {error}')
        return server_error(str(error))


def load_opis_from_korpus(izvor_id):
    """
    Ucitava opis izvora za dati ID izvora u korpusu
    """
    if not izvor_id:
        return None
    try:
        url = f'{settings.SEARCH_ENGINE_URL}/naslov/{izvor_id}'
        resp = http_requests.get(url)
        if resp.status_code == 200:
            entry = resp.json()
            return {
                'pub_id': entry['original_id'],
                'skracenica': entry['skracenica'],
                'opis': entry['opis'],
            }
        return None
    except Exception:
        return None


@api_view(['GET'])
def load_opis_from_korpus_wrapped(request, izvor_id):
    retval = load_opis_from_korpus(izvor_id)
    if retval is None:
        return Response(None, status=HTTP_404_NOT_FOUND, content_type=JSON)
    return Response(retval, status=HTTP_200_OK, content_type=JSON)
