from elasticsearch.exceptions import ElasticsearchException, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Bool, Match
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from .serializers import *
from .config import *
from .indexer import create_index_if_needed, save_odrednica_dict
from .cyrlat import sort_key

JSON = 'application/json'


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def odrednica(request):
    create_index_if_needed()

    if request.method == 'GET':
        return _search_odrednica(request)
    elif request.method == 'POST':
        return _add_odrednica(request)
    elif request.method == 'PUT':
        return _update_odrednica(request)
    elif request.method == 'DELETE':
        return _delete_odrednica(request)


def sort_key_composite(word):
    rbr_homo = word['rbr_homo'] if word['rbr_homo'] else 0
    result = sort_key(word['ociscena_rec'])
    result.append(rbr_homo)
    return result


def _search_odrednica(request):
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    hits = []
    s = Search(index=ODREDNICA_INDEX).source(includes=['pk', 'rec', 'vrsta', 'rbr_homo']).query(MultiMatch(
        type='bool_prefix',
        query=remove_punctuation(term),
        fields=['varijante'],
        # analyzer=SERBIAN_ANALYZER
    ))[0:100]
    try:
        response = s.execute()
        for hit in response.hits.hits:
            hits.append(hit['_source'])

        serializer = OdrednicaResponseSerializer(hits, many=True)
        result = sorted(serializer.data, key=lambda w: sort_key_composite(w))

        return Response(result, status=HTTP_200_OK)
    except ElasticsearchException as error:
        return server_error(error.args)


def _add_odrednica(request):
    if not request.data or request.data['odrednica'] is None:
        return bad_request('no data to index')
    odrednica = request.data['odrednica']

    return _save_odrednica(odrednica)


def _update_odrednica(request):
    if not request.data or request.data['odrednica'] is None:
        return bad_request('no data to index')
    odrednica = request.data['odrednica']

    return _save_odrednica(odrednica)


def _delete_odrednica(request):
    if not request.data or request.data['pk'] is None:
        return bad_request('no primary key')

    pk = request.data['pk']
    odrednica = OdrednicaDocument()
    try:
        odrednica.delete(id=pk, index=ODREDNICA_INDEX)
        return Response(status=HTTP_200_OK)
    except NotFoundError:
        return not_found('requested object not found')
    except ElasticsearchException as error:
        return server_error(error.args)


def _save_odrednica(item):
    serializer = CreateOdrednicaDocumentSerializer()
    try:
        result = save_odrednica_dict(item)
        return Response(result, status=HTTP_200_OK, content_type=JSON)
    except KeyError as ke:
        return bad_request(ke.args)
    except ElasticsearchException as ee:
        return server_error(ee.args)


def _delete_odrednica_by_id(id):
    odrednica = OdrednicaDocument()
    try:
        odrednica.delete(id=pk, index=ODREDNICA_INDEX)
        return Response(status=HTTP_200_OK)
    except NotFoundError:
        return not_found('requested object not found')
    except ElasticsearchException as error:
        return server_error(error.args)


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
    s = Search(index=ODREDNICA_INDEX)
    s = s.source(includes=['pk', 'rec', 'vrsta', 'rbr_homo'])
    s.query = MultiMatch(
        type='bool_prefix',
        query=remove_punctuation(term),  # clear_accents_old(term),
        fields=['varijante'],
    )
    try:
        response = s.execute()
        for hit in response.hits.hits:
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

        serializer = OdrednicaResponseSerializer(hits, many=True)
        data = serializer.data

        return Response(
            data,
            status=HTTP_200_OK,
            content_type=JSON
        )
    except ElasticsearchException as error:
        return server_error(error.args)


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
def load_opis_from_korpus(request, izvor_id):
    """
    Ucitava opis izvora za dati ID izvora u korpusu
    """
    query = {
        'query': {'term': {'pk': izvor_id}},
        'size': 1,
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
    if len(retval) == 0:
        return Response(None, status=HTTP_404_NOT_FOUND, content_type=JSON)
    return Response(retval[0], status=HTTP_200_OK, content_type=JSON)


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
