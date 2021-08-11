from elasticsearch.exceptions import ElasticsearchException, NotFoundError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Bool, Match
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from .serializers import *
from .config import *
from .indexer import create_index_if_needed, save_odrednica_dict

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


def _search_odrednica(request):
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    hits = []
    s = Search(index=ODREDNICA_INDEX)
    s = s.source(includes=['pk', 'rec', 'vrsta', 'rbr_homo'])
    s.query = MultiMatch(
        type='bool_prefix',
        query=clear_text(term),
        fields=['varijante'],
        # analyzer=SERBIAN_ANALYZER
    )
    try:
        response = s.execute()
        for hit in response.hits.hits:
            hits.append(hit['_source'])

        serializer = OdrednicaResponseSerializer(hits, many=True)
        data = serializer.data

        return Response(
            data,
            status=HTTP_200_OK,
            content_type=JSON
        )
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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def korpus(request):
    create_index_if_needed()

    if request.method == 'GET':
        return _search_korpus(request)
    elif request.method == 'POST':
        return _add_korpus(request)
    elif request.method == 'PUT':
        return _update_korpus(request)
    elif request.method == 'DELETE':
        return _delete_korpus(request)


def _search_korpus(request):
    if not request.data or request.data['term'] is None:
        return bad_request('no search term')

    term = request.data['term']
    hits = []
    s = Search(index=KORPUS_INDEX)
    s = s.source(includes=['pk', 'osnovniOblik'])
    s.query = Bool(
        must=[Match(oblici=term)]
    )
    try:
        response = s.execute()
        for hit in response.hits.hits:
            hits.append(hit['_source'])

        serializer = KorpusResponseSerializer(hits, many=True)
        data = serializer.data

        return Response(
            data,
            status=HTTP_200_OK,
            content_type=JSON
        )
    except ElasticsearchException as error:
        return server_error(error.args)


def _add_korpus(request):
    if not request.data or request.data['anotiranaRec'] is None:
        return bad_request('no data to index')
    anotiranaRec = request.data['anotiranaRec']

    return _save_korpus(anotiranaRec)


def _update_korpus(request):
    if not request.data or request.data['anotiranaRec'] is None:
        return bad_request('no data to index')
    anotiranaRec = request.data['anotiranaRec']

    return _save_korpus(anotiranaRec)


def _delete_korpus(request):
    if not request.data or request.data['pk'] is None:
        return bad_request('no primary key')

    pk = request.data['pk']
    anotiranaRec = KorpusDocument()
    try:
        anotiranaRec.delete(id=pk, index=KORPUS_INDEX)
        return Response(status=HTTP_200_OK)
    except NotFoundError:
        return not_found('requested object not found')
    except ElasticsearchException as error:
        return server_error(error.args)


def _save_korpus(item):
    serializer = CreateKorpusDocumentSerializer()
    try:
        anotiranaRec = serializer.create(item)
    except KeyError as error:
        return bad_request(error.args)

    try:
        result = anotiranaRec.save(id=anotiranaRec.pk, index=KORPUS_INDEX)
        return Response(
            result,
            status=HTTP_200_OK,
            content_type=JSON
        )
    except ElasticsearchException as error:
        return server_error(error.args)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def publikacija(request):
    create_index_if_needed()
    if request.method == 'GET':
        return _search_publikacija(request)
    # elif request.method == 'POST':
    #     return _add_publikacija(request)
    # elif request.method == 'PUT':
    #     return _update_publikacija(request)
    # elif request.method == 'DELETE':
    #     return _delete_publikacija(request)
    return server_error({})


def _search_publikacija(request):
    if not request.GET.get('q'):
        return bad_request('no search term')

    term = request.GET.get('q')
    hits = []
    s = Search(index=PUBLIKACIJE_INDEX)
    s = s.source(includes=['pk', 'skracenica', 'naslov'])
    s.query = MultiMatch(
        type='bool_prefix',
        query=term,
        fields=['tekst'],
    )
    try:
        response = s.execute()
        for hit in response.hits.hits:
            hits.append(hit['_source'])

        serializer = PublikacijaResponseSerializer(hits, many=True)
        data = serializer.data

        return Response(data, status=HTTP_200_OK, content_type=JSON)
    except ElasticsearchException as error:
        return server_error(error.args)


@api_view(['GET'])
def check_duplicate(request):
    term = request.GET.get('q')
    sid = request.GET.get('id')
    shomo = request.GET.get('homo')
    termid = int(sid) if sid else None
    rbr_homo = int(shomo) if shomo else None
    hits = []
    s = Search(index=ODREDNICA_INDEX)
    s = s.source(includes=['pk', 'rec', 'vrsta', 'rbr_homo'])
    s.query = MultiMatch(
        type='bool_prefix',
        query=clear_text(term),  # clear_accents_old(term),
        fields=['varijante'],
    )
    try:
        response = s.execute()
        for hit in response.hits.hits:
            try:
                found_homo = hit['_source']['rbr_homo']
            except KeyError:
                found_homo = None
            if hit['_source']['rec'] == term and termid is None:
                if found_homo and found_homo == rbr_homo:
                    hits.append(hit['_source'])
            if hit['_source']['rec'] == term and termid is not None and hit['_source']['pk'] != termid:
                if found_homo and found_homo == rbr_homo:
                    hits.append(hit['_source'])
        serializer = OdrednicaResponseSerializer(hits, many=True)
        data = serializer.data

        return Response(
            data,
            status=HTTP_200_OK,
            content_type=JSON
        )
    except ElasticsearchException as error:
        return server_error(error.args)


def bad_request(error):
    return Response(error, status=HTTP_400_BAD_REQUEST, content_type=JSON)


def not_found(error):
    return Response(error, status=HTTP_404_NOT_FOUND, content_type=JSON)


def server_error(error):
    return Response(error, status=HTTP_500_INTERNAL_SERVER_ERROR, content_type=JSON)
